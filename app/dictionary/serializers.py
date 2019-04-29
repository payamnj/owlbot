from rest_framework import serializers
from image_cropping.utils import get_backend
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


class EnrichedDefinitionSerializer(DefinitionSerializer):

    image_url = serializers.SerializerMethodField(required=False)

    def get_image_url(self, obj):
        if obj.image and obj.image_approved:
            url = get_backend().get_thumbnail_url(
                obj.image,
                {
                    'size': (400, 400),
                    'box': obj.cropping,
                    'crop': True,
                    'detail': True,
                }
            )
            return url
        else:
            return None

    class Meta:
        model = models.Defenition
        fields = ('type', 'definition', 'example', 'image_url')


class DictionarySerializer(serializers.Serializer):
    definitions = EnrichedDefinitionSerializer(many=True)
    word = serializers.CharField()
    pronunciation = serializers.CharField()

    class Meta:
        model = models.Defenition
        fields = ('word', 'pronunciation', 'definitions')