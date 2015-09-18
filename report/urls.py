from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^view/$', views.select, name='select'),
    url(r'^view/(?P<account_id>[0-9]+)/$', views.grandview, name="grandview"),
    url(r'^view/(?P<gcampaign_id>[0-9]+)/(?P<fbacc_id>[0-9]+)/$', views.select_adgroup, name='select_adgroup'),
    url(r'^view/(?P<gcampaign_id>[0-9]+)/(?P<fbacc_id>[0-9]+)/(?P<gadgroup_id>[0-9]+)/$', views.show_results, name='show_results'),
    url(r'^generate/(?P<start_date>[-A-Za-z0-9_]+)/(?P<end_date>[-A-Za-z0-9_]+)/$', views.getid, name='getid'),
    url(r'^generate/(?P<start_date>[-A-Za-z0-9_]+)/(?P<end_date>[-A-Za-z0-9_]+)/(?P<ccid>[0-9]+)/$', views.collect, name='collect'), 
    url(r'^spreadsheet/(?P<account_id>[0-9]+)/$', views.download, name='download'),
    url(r'^privacypolicy/$', views.privacypolicy, name='privacypolicy'),
    #url(r'^view/$', views.select, name = 'select'),
    #url(r'^campaigns/', views.campaigns, name='campaigns'),
    #url(r'^adgroups/(?P<adgroup_id>[0-9]+)', views.adgroup, name = 'adgroup'),
    #url(r'^login/', views.login, name = 'login'),
    #url(r'^(?P<campaign_id>[0-9]+)', views.result, name='result'),
    #url(r'^generate/(?P<time_id>[0-9]+)/$', views.main, name='main'),
    ]

