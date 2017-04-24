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
            ('cid', '555'),
            ('t', 'pageview'),
            ('dp', '/api/v1/dictionary/%s' % kwargs['word']),
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
    url = '/api/v1/dictionary/owl'


class DefenitionApi(APIView, GA):

    serializer_class = serializers.DefenitionSerializer

    def get(self, request, format=None, **kwargs):
        try:
            defenitions = models.Defenition.objects.filter(**{
                'word__word': kwargs['word'],
                'published': True
            })

            serializer = self.serializer_class(
                defenitions, many=True, context={'request': request})
            self.ga(request, **kwargs)
            output = serializer.data
            try:
                output[0]['message'] = 'OwlBot is a free API service but it has hosting costs, If you found it useful, please support me by your donation at https://www.paypal.me/payamnj'
            except:
                pass
            return Response(output)
        except ObjectDoesNotExist:
            return Response([{
                'result': '0', 'message': 'No defenition :('}])
