from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):

    def handle(self, *args, **options):
        Defenition = apps.get_model('dictionary', 'Defenition')
        defenitions = Defenition.objects.all()
        for defenition in defenitions:

            if defenition.example:
                example = defenition.example
                if example.startswith('"') and example.endswith('"'):
                    print(example)
                    defenition.example = example[1:-1]
                    defenition.save()
