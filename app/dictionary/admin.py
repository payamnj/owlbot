from django.contrib import admin
from django.db.models import Q
from django.utils import timezone
from app.dictionary import models
from image_cropping import ImageCroppingMixin
from easy_thumbnails.files import get_thumbnailer
from django.utils.safestring import mark_safe


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


def approve_image(modeladmin, request, queryset):
    queryset.update(image_approved=True)

approve_image.short_description = "Approve selected images"


class DefinitionAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_filter = ['type', 'published', 'image_approved',HasImage]
    list_display = ['word', 'defenition', 'published', 'has_image', 'type']
    fields = ('defenition', 'image', 'type', 'example', 'cropping')
    search_fields = ('word__word', 'defenition', )
    actions = [approve_image]

    def has_image(self, obj):
        return True if obj.image.name else False

    def display_image(self, obj):
        if not obj.image.name:
            return ""
        else:
            return mark_safe("<img src='https://media.owlbot.info/{}' width='100px' />".format(obj.image.name))

    def save_model(self, request, obj, form, change):
        if not obj.image_uploaded_at:
            obj.image_uploaded_at = timezone.localtime(timezone.now())
            obj.image_uploaded_by = request.user
        super().save_model(request, obj, form, change)

    def get_fields(self, request, obj=None):
        if request.user.groups.filter(name='image_publisher').exists():
            return ['image', 'cropping', 'defenition', 'type']
        else:
            return ('defenition', 'image', 'type', 'example', 'cropping', 'image_approved')

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='image_publisher').exists():
            return ['defenition', 'type']
        else:
            return []

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ['word', 'defenition', 'published', 'display_image', 'type', 'image_approved']
        return self.list_display

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if 'approve_image' in actions:
                del actions['approve_image']
        return actions


admin.site.register(models.Word, WordAdmin)
admin.site.register(models.Defenition, DefinitionAdmin)
