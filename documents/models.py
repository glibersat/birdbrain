from django.db import models


class Document(models.Model):
    uri = models.URLField(unique=True)
