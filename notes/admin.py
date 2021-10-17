from django.contrib import admin

from .models import Note, Statement


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    pass


@admin.register(Statement)
class StatementAdmin(admin.ModelAdmin):
    pass
