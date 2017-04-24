from django.core.management.base import BaseCommand
from django.db import connections
from app.dictionary import models


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Starting ... ')

        cursor = connections['anki'].cursor()
        sub_cursor = connections['anki'].cursor()
        cursor.execute("SELECT id, word \
            FROM anki_word")

        for row in cursor.fetchall():
            new_word = models.Word(**{
                'word': row[1]
            })
            new_word.save()
            sub_cursor.execute("SELECT type, defenition, example \
                from anki_defenition where word_id = %d" % row[0])

            for defenition in sub_cursor.fetchall():
                new_defenition = models.Defenition(**{
                    'word': new_word,
                    'type': defenition[0],
                    'defenition': defenition[1],
                    'example': defenition[2]
                })
                new_defenition.save()
