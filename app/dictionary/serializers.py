from rest_framework import serializers

import models


class DefenitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Defenition
        fields = ('type', 'defenition', 'example')
