import tempfile
import urllib.request
from urllib.request import urlopen

import magic
import speech_recognition as sr
from bs4 import BeautifulSoup
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, reverse
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from pydub import AudioSegment

from .forms import AudioTranscriptForm, DocumentUploadForm
from .models import Annotation, AudioDocument, Document


class DocumentImport(CreateView):
    """Import a Document"""

    model = Document
    fields = ["uri"]

    template_name = "documents/document_import.html"

    def scrap_uri(self, form):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
            "Accept-Encoding": "none",
            "Accept-Language": "en-US,en;q=0.8",
            "Connection": "keep-alive",
        }

        url = form.cleaned_data["uri"]
        request = urllib.request.Request(url)
        for name, value in headers.items():
            request.add_header(name, value)

        with urlopen(request) as f:
            soup = BeautifulSoup(f, "lxml")
            form.instance.content_raw = str(soup)

    def form_valid(self, form):
        self.scrap_uri(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("documents-document-detail", args=(self.object.pk,))


class DocumentDetail(DetailView):
    model = Document


class DocumentList(ListView):
    """List all Documents"""

    model = Document
    context_object_name = "documents"


def document_upload(request):
    if request.method == "POST":
        form = DocumentUploadForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.cleaned_data.get("file", False)
            if not file:
                return redirect("documents-document-import")

            # Guess file type
            filetype = magic.from_buffer(file.read(), mime=True)

            document = None
            print(filetype)
            # Audio file
            if filetype == "audio/mpeg":
                document = AudioDocument.objects.create(
                    format="mp3", file=request.FILES["file"]
                )

            if document:
                return redirect(document.get_absolute_url())

    return redirect("documents-document-import")


class AudioDocumentDetail(DetailView):
    model = AudioDocument
    template_name = "documents/audio_detail.html"
    context_object_name = "document"


def transcript_audio_region(request, pk):
    """Transcript a given region from an audio document"""
    doc = get_object_or_404(AudioDocument, pk=pk)

    if request.method == "POST":
        form = AudioTranscriptForm(request.POST)
        if form.is_valid():
            audio = AudioSegment.from_file("media/audio.mp3", format="mp3")
            start = float(form.cleaned_data["start"])
            start_ms = start * 1000  # in ms
            end = float(form.cleaned_data["end"])
            end_ms = end * 1000  # in ms
            if (end - start) <= 0:
                return HttpResponseBadRequest("Region should be positive")

            region = audio[start_ms:end_ms]

            with tempfile.NamedTemporaryFile(suffix=".wav") as fp:
                region.export(fp.name, format="wav")

                # Try transcription
                r = sr.Recognizer()
                with sr.AudioFile(fp.name) as source:
                    record = r.record(source)
                    text = r.recognize_google(record, language="fr-FR")

                    annotation, created = Annotation.objects.get_or_create(
                        document=doc, start=start, end=end
                    )
                    annotation.text = text
                    annotation.save()

                return redirect("documents-audio-detail", pk=doc.pk)
        else:
            return HttpResponseBadRequest("Invalid Form parameters")

    return HttpResponseBadRequest("GET not allowed")
