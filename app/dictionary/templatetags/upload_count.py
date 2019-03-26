from django import template
from app.dictionary.models import Defenition

register = template.Library()

@register.simple_tag(takes_context=True)
def upload_count(context):
    request = context['request']
    count = Defenition.objects.filter(image_uploaded_by=request.user, published=True).count()
    return count
