import urllib.request
from urllib.request import urlopen

from bs4 import BeautifulSoup
from django.shortcuts import reverse
from django.views.generic import CreateView, DetailView, ListView

from .models import Document


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
        # form.instance.content_plain = document.text_content()

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
