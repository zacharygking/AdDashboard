from django.shortcuts import render
from django.http import HttpResponse
from fb.models import Campaign, Account
from report.models import Keyword
from .models import Google, Facebook

def main(request):
	Google.objects.all().delete()
	google_clicks = 0
	google_impressions = 0
	google_cost = 0
	
	for current_google in Keyword.objects.all():
		google_clicks = google_clicks + current_google.clicks
		google_impressions = google_impressions + current_google.impressions
		google_cost = google_cost + current_google.cost
	
	google_model = Google()
	google_model.clicks = google_clicks
	google_model.impressions = google_impressions
	google_model.cost = round(google_cost,2)
	google_model.save()

	Facebook.objects.all().delete()
	facebook_clicks = 0
	facebook_impressions = 0
	facebook_cost = 0

	for current_facebook in Campaign.objects.all():
		facebook_clicks = facebook_clicks + current_facebook.clicks
		facebook_impressions = facebook_impressions + current_facebook.impressions
	
	for current_facebook in Account.objects.all():
		facebook_cost = facebook_cost + current_facebook.account_cost
		
	facebook_model = Facebook()
	facebook_model.clicks = facebook_clicks
	facebook_model.impressions = facebook_impressions
	facebook_model.cost = round(facebook_cost,2)
	facebook_model.save()
	
	return HttpResponse('success')
