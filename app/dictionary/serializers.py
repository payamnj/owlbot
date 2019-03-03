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


class EnrichedDefinitionSerializer(DefinitionSerializer):

    image_url = serializers.SerializerMethodField(required=False)

    def get_image_url(self, obj):
        if obj.image:
            return 'https://media.owlbot.info/{}'.format(obj.image.name)
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