# encoding: utf-8

"""
Urls for notes application

"""


from django.urls import path

from . import views

urlpatterns = [
    path("note/", views.NoteList.as_view(), name="notes-note-list"),
    path("note/create", views.NoteCreate.as_view(), name="notes-note-create"),
    path("note/<int:pk>", views.NoteDetail.as_view(), name="notes-note-detail"),
    path(
        "note/<int:note_id>/statement/add",
        views.note_statement_add,
        name="notes-note-statement-add",
    ),
    path("literal/<int:literal_id>", views.literal_detail, name="notes-literal-detail"),
]
