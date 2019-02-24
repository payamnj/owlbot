from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=200, null=True, unique=True)

    def __str__(self):
        return self.word


class Defenition(models.Model):
    word = models.ForeignKey(Word, related_name='defenition', on_delete=models.CASCADE)
    type = models.CharField(max_length=50, null=True)
    defenition = models.TextField(default='')
    synonyms = models.ManyToManyField(Word, related_name='synonyms')
    example = models.TextField(null=True)
    published = models.BooleanField(default=True)

    def __str__(self):
        return '%d- %s(%s)' % (self.id, self.word.word, self.type)
