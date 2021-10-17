from django import forms
from django.forms import formset_factory

from .models import Statement


class StatementForm(forms.Form):
    subject = forms.CharField()
    predicate = forms.CharField()
    object = forms.CharField()

    class Meta:
        fields = ["subject", "predicate", "object"]
