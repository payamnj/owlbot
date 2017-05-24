from rest_framework import serializers

import models


class DefenitionSerializer(serializers.ModelSerializer):
    
    test_field = serializers.SerializerMethodField()
    
    def get_test_field(self, obj):
        return 'test'

    class Meta:
        model = models.Defenition
        fields = ('type', 'defenition', 'example', 'test_field')
