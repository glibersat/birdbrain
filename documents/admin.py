from django.contrib import admin

from .models import Annotation, AudioDocument, Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(AudioDocument)
class AudioDocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    pass
