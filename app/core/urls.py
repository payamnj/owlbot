from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from app.dictionary import views as dictionary_views


api_v1_urlpatterns = [

    url(r'^dictionary/(?P<word>[\w\d]+)/?$',
        dictionary_views.DefenitionApi.as_view(),
        name='defenition_api'),
]

urlpatterns = [
    url(r'^joghdadmin/', include(admin.site.urls)),
    url(r'^/?$', dictionary_views.Home.as_view()),
    url(r'^api/v1/', include(api_v1_urlpatterns)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
