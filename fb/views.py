from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse('jae')
def get_report(request):
	return HttpResponse('song')


# Create your views here.