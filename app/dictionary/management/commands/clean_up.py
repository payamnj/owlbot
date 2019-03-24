from django.core.management.base import BaseCommand
from app.dictionary.models import Defenition, Word

from html.parser import HTMLParser




class Command(BaseCommand):

    def handle(self, *args, **options):
        r = Word.objects.filter(tmp_checked=False, pronunciation__isnull=True)
        print(r.count())
