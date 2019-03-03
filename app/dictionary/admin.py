from django.contrib import admin
from app.dictionary import models


class DefenitionInline(admin.StackedInline):
    fields = ('type', 'defenition', 'example', 'published')
    model = models.Defenition
    extra = 0


class WordAdmin(admin.ModelAdmin):
    search_fields = ['word', 'defenition__defenition']
    list_display = ['word', 'pronunciation']
    inlines = [
        DefenitionInline,
    ]


class DefinitionAdmin(admin.ModelAdmin):
    list_filter = ['type', 'published']
    list_display = ('word', 'defenition', 'published')
    fields = ('defenition', 'image')
    search_fields = ('defenition', )


admin.site.register(models.Word, WordAdmin)
admin.site.register(models.Defenition, DefinitionAdmin)