import re

from django.contrib.auth.models import User
from django.db.models import Count
from django.http.response import HttpResponseRedirectBase
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

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
        if not self.request.GET.get('q'):
            words = models.Word.objects.annotate(count=Count('definition')).filter(count__lte=5,
                                                                                   definition__image_approved=True)
            rand_num = random.randint(0, words.count())
            rand_word = words[rand_num]
        else:
            rand_word = get_object_or_404(models.Word.objects.filter(word=self.request.GET.get('q')).distinct(),
                                          definition__published=True)

        defenitions = models.Defenition.objects.filter(word=rand_word, published=True)
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


class GetToken(APIView, GA):

    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return super(GetToken, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return Response([{'message': 'Invalid email address'}], status=400)
        user, created = User.objects.get_or_create(email=email, defaults={'username': email})
        if not created:
            return Response([{'message': 'email address is already registered.'}], status=409)
        token = Token.objects.create(user=user)
        response = send_email(email, 'OWLBOT API Token',
                              '<div class=\'line-height: 25px;\'>Hey,<br/>We are glad that you have decided to use the OwlBot API.<br />'
                              'Your API token is: <b>{token}</b><br /><br />Here is a sample curl request for you: <br />'
                              '<div style=\'background-color: #353c44; color: #e0e0e0; margin: 14px 0; padding: 10px; border-radius: 4px\'>'
                              'curl --header "Authorization: Token {token}" https:<span>//owlbot</span>.<span>info</span>/api/v3/dictionary/owl -s | json_pp'
                              '</div>'
                              'Good Luck 🦉'
                              '</div>'.format(token=token.key))
        if response.status_code == 202:
            return Response([{'message': '👍 Token has been sent to the email address'}], status=202)
        else:
            user.delete()
            token.delete()
            return Response([{'message': 'Error on sending the email. Please try again later.'}])


def send_email(email, subject, content):
    message = Mail(
        from_email='owlbot@owlbot.info',
        to_emails=email,
        subject=subject,
        html_content=content)

    sg = SendGridAPIClient(settings.SENDGRID_API_TOKEN)
    response = sg.send(message)
    return response
