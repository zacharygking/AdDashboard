from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^(?P<campaign_id>[0-9]+)', views.result, name='result'),
    url(r'^generate/', views.main, name='main'),
    url(r'^campaigns/', views.campaigns, name='campaigns'),
    #url(r'campaigns/(?P<campaign_id>[0-9]+)', views.cdetail, name = 'cdetial'),
    ]

