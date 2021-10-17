import nltk
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView

from .forms import StatementForm
from .models import Literal, Note, Predicate, Statement


class Home(TemplateView):
    template_name = "home/home.html"


class NoteDetail(DetailView):
    model = Note

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tokens = nltk.tokenize.word_tokenize(self.object.content)
        allWords = [word for word in tokens if word.isalpha()]
        stopwords = nltk.corpus.stopwords.words("english")

        allWordExceptStopDist = nltk.FreqDist(
            w.lower() for w in allWords if w not in stopwords
        )

        context["words"] = allWordExceptStopDist.most_common(5)

        context["statement_form"] = StatementForm()
        return context


class NoteCreate(CreateView):
    """Create a Note"""

    model = Note
    fields = ["content", "source"]

    def get_success_url(self):
        return reverse("notes-note-detail", args=(self.object.pk,))


class NoteList(ListView):
    """List all Notes"""

    model = Note
    context_object_name = "notes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.query
        return context

    def get_queryset(self):
        query = self.request.GET.get("query", None)
        self.query = query

        if query:
            for word in query.split():
                queryset = self.model.objects.filter(
                    Q(content__icontains=word)
                    # | Q(subtitle__icontains=word)
                )
        else:
            queryset = self.model.objects.all()

        return queryset


def note_statement_add(request, note_id):
    """Add a statement to an existing Note, creating objects if necessary"""
    note = get_object_or_404(Note, pk=note_id)
    if request.method == "POST":
        form = StatementForm(request.POST)

        if form.is_valid():
            subject_t = form.cleaned_data["subject"]
            predicate_t = form.cleaned_data["predicate"]
            object_t = form.cleaned_data["object"]

            l_subject, created = Literal.objects.get_or_create(label=subject_t)
            l_predicate, created = Predicate.objects.get_or_create(label=predicate_t)
            l_object, created = Literal.objects.get_or_create(label=object_t)

            statement, created = Statement.objects.get_or_create(
                subject=l_subject, predicate=l_predicate, object=l_object
            )

            note.statements.add(statement)
            note.save()

    return redirect("notes-note-detail", pk=note_id)


def literal_detail(request, literal_id):
    literal = get_object_or_404(Literal, pk=literal_id)
    return render(
        request, template_name="notes/literal_detail.html", context={"literal": literal}
    )
