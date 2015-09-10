from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^test/', views.main, name='main'),
    url(r'^download/', views.download, name='download')
]
