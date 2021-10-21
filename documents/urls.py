# encoding: utf-8

"""
Urls for documents application

"""


from django.urls import path

from . import views

urlpatterns = [
    path(
        "document/import",
        views.DocumentImport.as_view(),
        name="documents-document-import",
    ),
    path(
        "document/",
        views.DocumentList.as_view(),
        name="documents-document-list",
    ),
    path(
        "document/upload",
        views.document_upload,
        name="documents-document-upload",
    ),
    path(
        "document/audio/<int:pk>",
        views.AudioDocumentDetail.as_view(),
        name="documents-audio-detail",
    ),
    path(
        "document/audio/<int:pk>/transcript",
        views.transcript_audio_region,
        name="documents-audio-transcript",
    ),
    path(
        "document/<int:pk>",
        views.DocumentDetail.as_view(),
        name="documents-document-detail",
    ),
    # path("literal/<int:literal_id>", views.literal_detail, name="notes-literal-detail"),
]
