from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from app.dictionary.models import Word
import requests


class Command(BaseCommand):

    def handle(self, *args, **options):
        faild_list = []
        while True:
            words = Word.objects.exclude(id__in=faild_list).filter(pronunciation__isnull=True)[:1000]
            if not words:
                break
            for word in words:
                print(word.word)
                if not get_pronunciation(word):
                    faild_list.append(word.id)

def get_pronunciation(word):
    try:
        response = requests.get('https://www.google.com/search?q=define+{}'.format(word.word), headers={
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"})
        content = response.content
        soup = BeautifulSoup(content)
        spans = soup.findAll("span", {"class": "lr_dct_ph"})
        p = spans[0].find('span').text
        print(p)
        word.pronunciation = p
        word.save()
        return True
    except Exception:
        return False
