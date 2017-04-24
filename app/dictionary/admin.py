from django.contrib import admin
import models


class DefenitionInline(admin.StackedInline):
    fields = ('type', 'defenition', 'example', 'published')
    model = models.Defenition
    extra = 0


class WordAdmin(admin.ModelAdmin):
    search_fields = ['word', 'defenition__defenition']
    inlines = [
        DefenitionInline,
    ]

admin.site.register(models.Word, WordAdmin)
