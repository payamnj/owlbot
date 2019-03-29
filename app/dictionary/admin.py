from django.contrib import admin
from django.db.models import Q
from django.utils import timezone
from app.dictionary import models
from image_cropping import ImageCroppingMixin


class DefenitionInline(admin.StackedInline):
    fields = ('type', 'defenition', 'example', 'published', 'image', 'cropping')
    model = models.Defenition
    extra = 0


class WordAdmin(admin.ModelAdmin):
    search_fields = ['word', 'defenition__defenition']
    list_display = ['word', 'pronunciation']
    inlines = [
        DefenitionInline,
    ]


class HasImage(admin.SimpleListFilter):
    title = 'has_image'
    parameter_name = 'has_image'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'No':
            return queryset.filter(Q(image='') | Q(image=None))
        elif value == 'Yes':
            return queryset.exclude(Q(image='') | Q(image=None))
        return queryset


class DefinitionAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_filter = ['type', 'published', HasImage]
    list_display = ('word', 'defenition', 'published', 'has_image', 'type')
    fields = ('defenition', 'image', 'type', 'example', 'cropping')
    search_fields = ('word__word', 'defenition', )

    def has_image(self, obj):
        return True if obj.image.name else False

    def save_model(self, request, obj, form, change):
        if not obj.image_uploaded_at:
            obj.image_uploaded_at = timezone.localtime(timezone.now())
            obj.image_uploaded_by = request.user
        super().save_model(request, obj, form, change)

    def get_fields(self, request, obj=None):
        if request.user.groups.filter(name='image_publisher').exists():
            return ['image', 'cropping', 'defenition', 'type']
        else:
            return  ('defenition', 'image', 'type', 'example', 'cropping', 'image_approved')

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='image_publisher').exists():
            return ['defenition', 'type']
        else:
            return []

admin.site.register(models.Word, WordAdmin)
admin.site.register(models.Defenition, DefinitionAdmin)
