from django.contrib import admin

from .models import Literal, Note, Predicate, Statement


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    pass


@admin.register(Statement)
class StatementAdmin(admin.ModelAdmin):
    pass


@admin.register(Literal)
class LiteralAdmin(admin.ModelAdmin):
    pass


@admin.register(Predicate)
class PredicateAdmin(admin.ModelAdmin):
    pass
