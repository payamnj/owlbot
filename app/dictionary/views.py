from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import RedirectView
import models
import serializers
import urllib2, urllib


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request):
    try:
        return request.META['HTTP_USER_AGENT']
    except:
        return 'Unknown'


class GA(object):

    def ga(self, request, **kwargs):
        post_data = [
            ('v', '1'),
            ('tid', 'UA-80200867-1'),
            ('cid', get_client_ip(request)),
            ('t', 'pageview'),
            ('dp', str(request.path)),
            ('dt', 'Dictionary Api (%s)' % kwargs['word']),
            ('uip', get_client_ip(request)),
            ('ua', get_user_agent(request))
        ]
        resp = urllib2.urlopen(
            'https://www.google-analytics.com/collect',
            urllib.urlencode(post_data)
        )

        content = resp.read()
        print(content)


class Home(RedirectView):
    url = '/api/v2/dictionary/owl'


class DefinitionApi(APIView, GA):

    def get_serializer_class(self):
        if '/v1/' in self.request.path:
            return serializers.DefenitionSerializer
        return serializers.DefinitionSerializer

    def get(self, request, format=None, **kwargs):
        try:
            defenitions = models.Defenition.objects.filter(**{
                'word__word': kwargs['word'],
                'published': True
            })

            serializer = self.get_serializer_class()(
                defenitions, many=True, context={'request': request})
            self.ga(request, **kwargs)
            output = serializer.data
            return Response(output)
        except ObjectDoesNotExist:
            return Response([{
                'result': '0', 'message': 'No defenition :('}])
