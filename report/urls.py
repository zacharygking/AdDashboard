from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^(?P<campaign_id>[0-9]+)', views.result, name='result'),
    url(r'^generate/(?P<time_id>[0-9]+)/$', views.main, name='main'),
    url(r'^generate/(?P<start_date>\w+)/(?P<end_date>\w+)/', views.collect, name='collect'),
    url(r'^campaigns/', views.campaigns, name='campaigns'),
    url(r'^adgroups/(?P<adgroup_id>[0-9]+)', views.adgroup, name = 'adgroup'),
    url(r'^login/', views.login, name = 'login')
    #url(r'campaigns/(?P<campaign_id>[0-9]+)', views.cdetail, name = 'cdetial'),
    ]

