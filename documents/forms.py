from django import forms

from . import models


class DocumentUploadForm(forms.Form):
    file = forms.FileField(required=True)


class AudioTranscriptForm(forms.Form):
    start = forms.FloatField(required=True)
    end = forms.FloatField(required=True)
