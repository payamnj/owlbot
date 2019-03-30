from django.db import models
from django.contrib.auth.models import User
from image_cropping import ImageRatioField


class Word(models.Model):
    word = models.CharField(max_length=200, null=True, unique=True)
    pronunciation = models.CharField(max_length=255, blank=True, null=True)
    tmp_checked = models.BooleanField(default=False)

    def __str__(self):
        return self.word


class Defenition(models.Model):
    word = models.ForeignKey(Word, related_name='defenition', on_delete=models.CASCADE)
    type = models.CharField(max_length=50, null=True)
    defenition = models.TextField(default='')
    synonyms = models.ManyToManyField(Word, related_name='synonyms')
    example = models.TextField(null=True, blank=True)
    published = models.BooleanField(default=True)
    image = models.ImageField(upload_to='dictionary/images', blank=True, null=True)
    image_uploaded_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    image_uploaded_at = models.DateTimeField(null=True, blank=True)
    cropping = ImageRatioField('image', '500x500')
    image_approved = models.BooleanField(default=False)

    def __str__(self):
        return '%d- %s(%s)' % (self.id, self.word.word, self.type)

    class Meta:
        verbose_name_plural = 'Definitions'
        verbose_name = 'Definition'
