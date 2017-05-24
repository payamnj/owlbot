from rest_framework import serializers

import models


class DefenitionSerializer(serializers.ModelSerializer):
    
    test_field = 'test'

    class Meta:
        model = models.Defenition
        fields = ('type', 'defenition', 'example', 'test_field')
