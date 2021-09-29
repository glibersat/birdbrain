from django.shortcuts import render
from django.views.generic.edit import CreateView

from notes.models import Note


class NoteCreate(CreateView):
    model = Note
    fields = ["content"]
