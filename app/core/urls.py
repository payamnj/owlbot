from django.conf.urls import include, url
from django.contrib import admin
from app.dictionary import views as dictionary_views
from django.urls import path


api_v1_urlpatterns = [
    url(r'^dictionary/(?P<word>[\w\d]+)/?$',
        dictionary_views.DefinitionApi.as_view(),
        name='definition_api'),
]

api_v2_urlpatterns = api_v1_urlpatterns

urlpatterns = [
    path('joghdadmin/', admin.site.urls),
    url(r'^$', dictionary_views.Home.as_view()),
    url(r'^api/v1/', include(api_v1_urlpatterns)),
    url(r'^api/v2/', include(api_v2_urlpatterns))
]
