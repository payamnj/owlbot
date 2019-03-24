from django.core.management.base import BaseCommand
from app.dictionary.models import Defenition, Word

from html.parser import HTMLParser



class Command(BaseCommand):

    def handle(self, *args, **options):
        of = 0
        while True:
            to_cleans = Word.objects.filter(word__contains=' ')[of:][:100]
            if not to_cleans:
                return
            of += 100
            for c in to_cleans:
                print(c.id)
                print(c.word)
