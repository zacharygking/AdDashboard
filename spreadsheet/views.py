from django.shortcuts import render
from django.http import HttpResponse
from fb.models import Campaign, Account
from report.models import Keyword
from .models import Metric
import django_excel as excel
import pyexcel.ext.xls

def main(request):
	Metric.objects.all().delete()
	
	google_clicks = 0
	google_impressions = 0
	google_cost = 0
	
	facebook_clicks = 0
	facebook_impressions = 0
	facebook_cost = 0
	
	for current_google in Keyword.objects.all():
		google_clicks = google_clicks + current_google.clicks
		google_impressions = google_impressions + current_google.impressions
		google_cost = google_cost + current_google.cost
	
	google_model = Metric()
	google_model.name = 'Google'
	google_model.clicks = google_clicks
	google_model.impressions = google_impressions
	google_model.cost = round(google_cost,2)
	google_model.save()

	for current_facebook in Campaign.objects.all():
		facebook_clicks = facebook_clicks + current_facebook.clicks
		facebook_impressions = facebook_impressions + current_facebook.impressions
	
	for current_facebook in Account.objects.all():
		facebook_cost = facebook_cost + current_facebook.account_cost
		
	facebook_model = Metric()
	facebook_model.name = 'Facebook'
	facebook_model.clicks = facebook_clicks
	facebook_model.impressions = facebook_impressions
	facebook_model.cost = round(facebook_cost,2)
	facebook_model.save()
	
	return HttpResponse('success')

def download(request):
	return excel.make_response_from_tables([Metric], 'xls')	
	
