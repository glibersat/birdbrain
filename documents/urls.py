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
        "document/<int:pk>",
        views.DocumentDetail.as_view(),
        name="documents-document-detail",
    ),
    # path("literal/<int:literal_id>", views.literal_detail, name="notes-literal-detail"),
]
