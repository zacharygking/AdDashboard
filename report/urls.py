from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<campaign_id>[0-9]+)', views.result, name='result'),
    url(r's/$', views.main, name='main')
    ]

