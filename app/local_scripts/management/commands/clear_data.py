from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):

    def handle(self, *args, **options):
        Defenition = apps.get_model('dictionary', 'Defenition')
        defenitions = Defenition.objects.all()

        unpublish_list = [
            'Australian/NZ', 'Physiology', 'historical', 'Billiards',
            'Military', 'Nautical', 'Anatomy', 'dialect', 'Greek Mythology',
            'see', 'Photography', 'Biology', 'Soccer', 'North American',
            'Astrology', 'formal', 'Entomology', 'Christian Theology',
            'Stock Exchange', 'Theology',  'American Football', 'urinate.',
            'Biochemistry', 'Medicine', 'Rugby', 'derogatory', 'dated',
            'Zoology', 'Genetics', 'Geology', 'Physics', 'Phonetics', 'vomit.',
            'vulgar slang', 'Law', 'Cricket', 'nonsense.', 'Baseball',
            'South African', 'Philosophy', 'Grammar', 'Scottish', 'Astronomy',
            'Architecture', 'Linguistics', 'Bridge', 'informal', 'Computing',
            'Logic', 'archaic', 'Irish', 'West Indian', 'literary', 'Canadian',
            'technical', 'Heraldry', 'Sailing', 'Geometry', 'Australian',
            'British', 'Statistics', 'Mathematics', 'Printing', 'Botany',
            'Music', 'trademark', 'steal.', 'Christian Church', 'a lesbian.',
            'Chemistry', 'rare', 'US', 'Finance', 'Golf', 'Electronics']

        for defenition in defenitions:

            if defenition.example:
                example = defenition.example
                if example.startswith('"') and example.endswith('"'):
                    print(example)
                    defenition.example = example[1:-1]
                    defenition.save()

            
            if defenition.defenition in unpublish_list:
                defenition.published = False
                defenition.save()

            

