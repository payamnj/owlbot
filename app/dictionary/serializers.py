from rest_framework import serializers

from app.dictionary import models


class DefenitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Defenition
        fields = ('type', 'defenition', 'example')
        

class DefinitionSerializer(serializers.ModelSerializer):

    definition = serializers.SerializerMethodField()
    
    def get_definition(self, obj):
        return obj.defenition

    class Meta:
        model = models.Defenition
        fields = ('type', 'definition', 'example')
