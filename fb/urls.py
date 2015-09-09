from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^generate/', views.get_report, name='generate'),
    url(r'^accounts/', views.accounts, name='accounts'),
    url(r'^campaigns/(?P<cid>[0-9]+)', views.campaigns, name='campaingns'),

]
