import pytest
from django.shortcuts import reverse
from model_bakery.recipe import Recipe

from notes import models


@pytest.mark.django_db
def test_create_new_note_and_redirect(client):
    content = "this is some content"

    response = client.post(
        reverse("notes-note-create"),
        data={"content": content},
    )
    note = models.Note.objects.all()[0]
    assert note.content == content
    assert response.status_code == 302
