from django.conf.urls import include, url
from django.contrib import admin
from app.dictionary import views as dictionary_views
from django.urls import path


api_urlpatterns = [
    url(r'^dictionary/(?P<word>[\w\d ]+)/?$',
        dictionary_views.DefinitionApi.as_view(),
        name='definition_api'),
    url(r'^get_token$',
        dictionary_views.GetToken.as_view(),
        name='get_token')
]


urlpatterns = [
    path('joghdadmin/', admin.site.urls),
    url(r'^$', dictionary_views.Home.as_view()),
    url(r'^api/(?P<version>v[123])/', include(api_urlpatterns))
]
