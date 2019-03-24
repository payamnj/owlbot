# Generated by Django 2.1.7 on 2019-03-23 18:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dictionary', '0007_word_tmp_checked'),
    ]

    operations = [
        migrations.AddField(
            model_name='defenition',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('image', '500x500', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropping'),
        ),
        migrations.AddField(
            model_name='defenition',
            name='image_uploaded_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='defenition',
            name='image_uploaded_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='defenition',
            name='example',
            field=models.TextField(blank=True, null=True),
        ),
    ]
