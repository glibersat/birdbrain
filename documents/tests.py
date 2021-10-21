import pytest
from django.urls import reverse
from model_bakery.recipe import Recipe

from .models import AudioDocument


@pytest.mark.django_db
def test_audio_transcript(client):
    document = Recipe(AudioDocument).make()
    response = client.post(
        reverse("documents-audio-transcript", args=(document.id,)),
        data={"start": 72.7, "end": 81.2},
    )

    assert response.status_code == 302
