from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from app.dictionary import views as dictionary_views


api_v1_urlpatterns = [
    url(r'^dictionary/(?P<word>[\w\d]+)/?$',
        dictionary_views.DefinitionApi.as_view(),
        name='definition_api'),
]

api_v2_urlpatterns = api_v1_urlpatterns

urlpatterns = [
    url(r'^joghdadmin/', include(admin.site.urls)),
    url(r'^/?$', dictionary_views.Home.as_view()),
    url(r'^api/v1/', include(api_v1_urlpatterns)),
    url(r'^api/v2/', include(api_v2_urlpatterns))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
