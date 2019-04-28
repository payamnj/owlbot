from django.db.models import Count
from django.http.response import HttpResponseRedirectBase
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View, TemplateView
from app.dictionary import models
from app.dictionary import serializers
import random
import requests
import logging


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
        if not request.user.username:
            username = 'Anonymous'
        else:
            username = request.user.username

        post_data = {
            'v': '1',
            'tid': 'UA-80200867-1',
            'cid': get_client_ip(request),
            't': 'pageview',
            'dp': str(request.path),
            'dt': 'Dictionary Api (%s)' % kwargs['word'],
            'uip': get_client_ip(request),
            'ua': get_user_agent(request),
            'cd1': username,
        }

        requests.post('https://www.google-analytics.com/collect', data=post_data, timeout=2)


class HttpResponseRedirectTemp(HttpResponseRedirectBase):
    status_code = 307


class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        words = models.Word.objects.annotate(count=Count('definition')).filter(count__lte=2, definition__image_approved=True)
        rand_num = random.randint(0, 50)
        rand_word = words[rand_num]
        defenitions = models.Defenition.objects.filter(word=rand_word)
        renderer = JSONRenderer()
        context['response'] = renderer.render(serializers.DictionarySerializer(
            {'word': rand_word.word, 'pronunciation': defenitions.first().word.pronunciation,
             'definitions': list(defenitions)}).data).decode()

        return context



class DefinitionApi(APIView, GA):

    def dispatch(self, request, *args, **kwargs):
        if kwargs['version'] == 'v3':
            self.permission_classes = (IsAuthenticated,)
        return super(DefinitionApi, self).dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.kwargs['version'] == 'v1':
            return serializers.DefenitionSerializer
        return serializers.DefinitionSerializer

    def get(self, request, format=None, **kwargs):
        try:
            defenitions = models.Defenition.objects.filter(**{
                'word__word': kwargs['word'],
                'published': True
            })
            if kwargs['version'] == 'v3':
                serializer = serializers.DictionarySerializer(
                    {'word': kwargs['word'], 'pronunciation': defenitions.first().word.pronunciation,
                     'definitions': list(defenitions)})
            else:
                serializer = self.get_serializer_class()(
                    defenitions, many=True, context={'request': request})

            self.ga(request, **kwargs)
            output = serializer.data
            return Response(output)
        except ObjectDoesNotExist:
            return Response([{
                'message': 'No definition :('}], status=404)
        except Exception as e:
            logging.exception(str(e), extra={'word': kwargs.get('word')})
            raise e
