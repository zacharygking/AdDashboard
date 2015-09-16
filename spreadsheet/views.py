from django.shortcuts import render
from django.http import HttpResponse
from report.models import GoogleKeyword, FacebookCampaign, FacebookAccount
from .models import Source
import django_excel as excel
import pyexcel.ext.xls

def main(request):
	Source.objects.all().delete()
	
	google_clicks = 0
	google_impressions = 0
	google_cost = 0
	
	facebook_clicks = 0
	facebook_impressions = 0
	facebook_cost = 0
	
	for current_google in GoogleKeyword.objects.all():
		google_clicks = google_clicks + current_google.clicks
		google_impressions = google_impressions + current_google.impressions
		google_cost = google_cost + current_google.cost
	
	google_model = Source()
	google_model.name = 'Google'
	google_model.clicks = google_clicks
	google_model.impressions = google_impressions
	google_model.cost = round(google_cost,2)
	google_model.save()

	for current_facebook in FacebookCampaign.objects.all():
		facebook_clicks = facebook_clicks + current_facebook.clicks
		facebook_impressions = facebook_impressions + current_facebook.impressions
		facebook_cost = facebook_cost + current_facebook.cost
		
	facebook_model = Source()
	facebook_model.name = 'Facebook'
	facebook_model.clicks = facebook_clicks
	facebook_model.impressions = facebook_impressions
	facebook_model.cost = round(facebook_cost,2)
	facebook_model.save()
	
	total = Source()
	total.name = 'TOTAL'
	total.clicks = google_model.clicks + facebook_model.clicks
	total.impressions = google_model.impressions + facebook_model.impressions 
	total.cost = google_model.cost + facebook_model.cost
	total.save()
	
	return HttpResponse('success')

def download(request):
	return excel.make_response_from_tables([Source], 'xls')	
	
