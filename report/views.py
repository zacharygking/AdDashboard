#!/usr/bin/python

#import for all
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from report.models import Report, Source, adSource, GoogleClient, GoogleCampaign, GoogleAdGroup, GoogleKeyword, FacebookCampaign, FacebookAccount

#import for google
import logging
import sys
import xml.etree.ElementTree as ET
from googleads import adwords
from django.core.exceptions import ObjectDoesNotExist
from allauth.socialaccount.models import SocialToken, SocialAccount
from report.forms import DateForm

#import for facebook
from facebookads.api import FacebookAdsApi
from facebookads import objects
from facebookads.objects import AdAccount
from facebookads.objects import AdCampaign
from allauth.socialaccount.models import SocialToken, SocialAccount
import json
import ast

#import for excel
import django_excel as excel
import pyexcel.ext.xls

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.transport').setLevel(logging.DEBUG)

def collect1(request,start_date,end_date,gcid,fcid):
  client = GoogleClient.objects.get(pk=gcid)
  client_id = client.client_id
  client_name = client.client_name
  
  #account = FacebookAccount.objects.get(account_name='Western Health Advantage')
  account = FacebookAccount.objects.get(pk=fcid)
  try:
    fb_acc = SocialAccount.objects.get(user_id = request.user.id,provider='facebook')
    #google_acc = SocialAccount.objects.get(user_id = request.user.id,provider='google')
    fb_tok = SocialToken.objects.get(account=fb_acc)
    #google_tok = SocialToken.objects.get(account=google_acc)
  except:
    return HttpResponse("error connecting Social Accounts")

  #clear the database
  GoogleCampaign.objects.all().delete()
  GoogleAdGroup.objects.all().delete()
  GoogleKeyword.objects.all().delete()

  #FacebookAccount.objects.all().delete()
  Report.objects.all().delete()

  report_model = Report()
  report_model.user = request.user.username
  report_model.date_taken = datetime.now()
  report_model.google_account = client_name

  if(start_date == '1' and end_date == '1'):
    report_model.date_range = "All Time"
    report_model.save()
    account.report = report_model
    account.save()
    all_google_data(request, client_id)
    return render(request, 'report/onetwo.html')
    return redirect("../2")
  elif(start_date == '2' and end_date == '2'):
    report_model.date_range = "Last 30 Days"
    report_model.save()
    account.report = report_model
    account.save()
    month_google_data(request, client_id)
    #"../../../../view"
    return render(request, 'report/onetwo.html') 
    return redirect("../2")
	
  i_y = start_date[0] + start_date[1] + start_date[2] + start_date[3]
  i_m = start_date[5] + start_date[6]
  i_d = start_date[8] + start_date[9]

  f_y = end_date[0] + end_date[1] + end_date[2] + end_date[3]
  f_m = end_date[5] + end_date[6]
  f_d = end_date[8] + end_date[9]


  googstartDate = i_y+i_m+i_d
  googendDate = f_y+f_m+f_d

  fbstartDate = i_y + '-' + i_m + '-' + i_d
  fbendDate = f_y + '-' + f_m + '-' + f_d

  report_model.date_range = fbstartDate + " to " + fbendDate
  report_model.save()
  
  account.report = report_model
  account.save()

  #get the google data
  google_data(request, client_id, googstartDate, googendDate)

  #get the facebook data

  
  return render(request, 'report/onetwo.html')
  return redirect("../2")

def collect2(request,start_date,end_date,gcid,fcid):
  client = GoogleClient.objects.get(pk=gcid)
  client_id = client.client_id
  client_name = client.client_name

  FacebookCampaign.objects.all().delete()
  account = FacebookAccount.objects.get(pk=fcid)
  report_model = Report.objects.get(user= request.user.username)

  if(start_date == '1' and end_date == '1'):
    all_fb_data(request, account)
    return render(request, 'report/twothree.html')
  elif(start_date == '2' and end_date == '2'):
    month_fb_data(request, account)
    return render(request, 'report/twothree.html')

  i_y = start_date[0] + start_date[1] + start_date[2] + start_date[3]
  i_m = start_date[5] + start_date[6]
  i_d = start_date[8] + start_date[9]

  f_y = end_date[0] + end_date[1] + end_date[2] + end_date[3]
  f_m = end_date[5] + end_date[6]
  f_d = end_date[8] + end_date[9]


  fbstartDate = i_y + '-' + i_m + '-' + i_d
  fbendDate = f_y + '-' + f_m + '-' + f_d

  fb_data(request, account, fbstartDate, fbendDate)

  return render(request, 'report/twothree.html')

def collect3(request,start_date,end_date,gcid,fcid):
  fb_organize()
  return render(request, 'report/threefour.html')

def collect4(request,start_date,end_date,gcid,fcid):
  g_organize()
  return render(request, 'report/fourfive.html')

def collect5(request,start_date,end_date,gcid,fcid):
	total()
	redir = "../../../../../../../../../../../view/" + str(gcid) + '/'+ str(fcid)
	return redirect(redir)
  
def fb_organize():
	adSource.objects.all().delete()
	for fb_group in FacebookAccount.objects.all():
		fb_name = fb_group.account_name
		category = adSource()
		category.provider = 'Facebook'
		category.name = fb_name
		
		for fb_cam in FacebookCampaign.objects.all():
			if fb_cam.account.account_name == fb_name:
				category.impressions = category.impressions + fb_cam.impressions
				category.cost = category.cost + fb_cam.cost
				category.clicks = category.clicks + fb_cam.clicks
				
		category.cost = round(category.cost,2)
		
		if not category.impressions == 0:
			category.CTR = round(category.clicks * 100/category.impressions,2)
			category.CPM = round(category.cost * 1000 / category.impressions,2)
		if not category.clicks == 0:
			category.CPC = round(category.cost/category.clicks,2)
		category.save()
  
def g_organize():
	'''
	adSource.objects.all().delete()
	
	for goog_cam in GoogleCampaign.objects.all():
		goog_name = goog_cam.campaign_name
		category = adSource()
		category.provider = 'Google'
		category.name = goog_name
		
		for goog_key in GoogleKeyword.objects.all():
			if goog_key.adgroup.campaign.campaign_name == goog_name:
				category.impressions = category.impressions + goog_key.impressions
				category.cost = round(category.cost,2) + round(goog_key.cost,2)
				category.clicks = category.clicks + goog_key.clicks
				
		category.cost = round(category.cost,2)
		
		if not category.impressions == 0:
			category.CTR = round(category.clicks * 100/category.impressions,2)
			category.CPM = round(category.cost * 1000 / category.impressions,2)
		if not category.clicks == 0:
			category.CPC = round(category.cost/category.clicks,2)
		category.save() 
		'''
	for goog_cam in GoogleCampaign.objects.all():
		goog_name = goog_cam.campaign_name
		category = adSource()
		category.provider = 'Google'
		category.name = goog_name
		
		for goog_ad in goog_cam.googleadgroup_set.all():
			for goog_key in goog_ad.googlekeyword_set.all():
			
				#if goog_key.adgroup.campaign.campaign_name == goog_name:
				category.impressions = category.impressions + goog_key.impressions
				category.cost = round(category.cost,2) + round(goog_key.cost,2)
				category.clicks = category.clicks + goog_key.clicks
				
		category.cost = round(category.cost,2)
		
		if not category.impressions == 0:
			category.CTR = round(category.clicks * 100/category.impressions,2)
			category.CPM = round(category.cost * 1000 / category.impressions,2)
		if not category.clicks == 0:
			category.CPC = round(category.cost/category.clicks,2)
		
		category.save() 

def total():
	Source.objects.all().delete()
	
	google_clicks = 0
	google_impressions = 0
	google_cost = 0

	for current_google in GoogleKeyword.objects.all():
		google_clicks = google_clicks + current_google.clicks
		google_impressions = google_impressions + current_google.impressions
		google_cost = google_cost + current_google.cost
	
	google_model = Source()
	google_model.name = 'Google'
	google_model.clicks = google_clicks
	google_model.impressions = google_impressions
	google_model.cost = round(google_cost,2)
	if not google_model.impressions == 0:
		google_model.CTR = round(google_model.clicks * 100/google_model.impressions,2)
		google_model.CPM = round(google_model.cost * 1000 / google_model.impressions,2)
	if not google_model.clicks == 0:
		google_model.CPC = round(google_model.cost/google_model.clicks,2)
	google_model.save()

def download(request, account_id):
	facebook_account = FacebookAccount.objects.get(account_id=account_id)
	facebook_adSource = adSource.objects.get(name=facebook_account.account_name)
	google = Source.objects.get(name='Google')
	addUp(google, facebook_adSource)
	query_sets = Source.objects.filter()
	column_names = ['name', 'clicks', 'impressions', 'CTR', 'CPC', 'CPM', 'cost']
	return excel.make_response_from_query_sets(query_sets, column_names, 'xls')

def addUp(google, facebook_adSource):
	Source.objects.filter(name='Facebook').delete()
	Source.objects.filter(name='TOTAL').delete()

	facebook = Source()
	facebook.name = 'Facebook'
	facebook.clicks = facebook_adSource.clicks
	facebook.impressions = facebook_adSource.impressions
	facebook.cost = facebook_adSource.cost
	facebook.CTR = facebook_adSource.CTR
	facebook.CPC = facebook_adSource.CPC
	facebook.CPM = facebook_adSource.CPM
	facebook.save()
	
	total = Source()
	total.name = 'TOTAL'
	total.clicks = google.clicks + facebook.clicks
	total.impressions = google.impressions + facebook.impressions 
	total.cost = google.cost + facebook.cost
	total.cost = round(total.cost,2)
	if not total.impressions == 0:	
		total.CTR = round(total.clicks * 100/total.impressions,2)
		total.CPM = round(total.cost * 1000/total.impressions,2)
	if not total.clicks == 0:		
		total.CPC = round(total.cost/total.clicks,2)
	total.save()

'''
	method will create a report downloader implemented by google 
	and fetch the data which will then be stored in a xml file 
	and the xml file will be parsed to store it on django server
'''
def google_data(request, client_id, startDate, endDate):
	try:
		google_client = GoogleClient.objects.get(client_id=client_id)
	except ObjectDoesNotExist:
		return HttpResponse('The Client ID does not exist')
	adwords_client = adwords.AdWordsClient.LoadFromStorage()
	adwords_client.SetClientCustomerId(client_id)
	report_downloader = adwords_client.GetReportDownloader(version='v201506')  
  
	# Create report definition.
	report = {
		'reportName': 'CRITERIA_PERFORMANCE_REPORT',
		'dateRangeType': 'CUSTOM_DATE',
		'reportType': 'CRITERIA_PERFORMANCE_REPORT',
		'downloadFormat': 'XML',
		'selector': {
			'fields': ['AccountDescriptiveName', 'AdGroupName', 'CampaignName',
						'Id', 'Criteria', 'Impressions', 'Clicks', 'Cost'],
			'dateRange': {'min': startDate,
							'max': endDate}
		}
	}
	file = open('output.xml', 'w')

	#creating the report downloader
	report_downloader.DownloadReport(
		report, file, skip_report_header=False, skip_column_header=False,
		skip_report_summary=False, include_zero_impressions=False)

	#save the file
	file.close()

	#parsing
	tree = ET.parse('output.xml')
	root = tree.getroot()

	#nested for loops to parse xml file
	for table in root.findall('table'):
		for row in table.findall('row'):
			
			#names are grabbed
			campaignName = row.get('campaign')
			adGroupName = row.get('adGroup')
			
			try:
				#does the campaign exist already
				campaign = GoogleCampaign.objects.get(campaign_name=campaignName)
			except ObjectDoesNotExist:
				#if not then make a new campaign
				campaign = GoogleCampaign()
				campaign.campaign_name = campaignName
				campaign.client = google_client
				campaign.save()
			
			try:
				#does the adgroup exist
				adGroup = GoogleAdGroup.objects.get(ad_group_name=adGroupName, campaign_name=campaignName)
			except ObjectDoesNotExist:
				#if not make a new
				adGroup = GoogleAdGroup()
				adGroup.ad_group_name = adGroupName                        
			
			#set the hierarchy of google data
			adGroup.campaign = campaign
			adGroup.campaign_name = campaignName
			adGroup.save()
			
			#create a new keyword for every entity
			data = GoogleKeyword()
			data.keyword_id = row.get('keywordID')
			data.keyword_placement = row.get('keywordPlacement')
			data.clicks = row.get('clicks')
			data.impressions = row.get('impressions')
			data.cost = row.get('cost')
			data.cost = str(float(data.cost)/1000000)
			data.adgroup = adGroup
			data.save()		

'''
	method does the same thing as google but it is for facebook
'''
def fb_data(request, account_model, fbstartDate, fbendDate):	

	try:
		fb_acc = SocialAccount.objects.get(user_id = request.user.id,provider='facebook')
		fb_tok = SocialToken.objects.get(account=fb_acc)
	except:
		return HttpResponse("error connecting Social Accounts")
	
	#setting the user information
	my_app_id = '1604519246476149'
	my_app_secret = ''
	my_access_token = fb_tok.token
	
	#gets the ad accounts in a single, pre-existing facebook account
	FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
	me = objects.AdUser(fbid='me')
	my_accounts = list(me.get_ad_accounts())

	#does it have ad accounts
	if len(my_accounts) == 0:
		return HttpResponse("no Ad Accounts Exist")
	
	#important note, facebook allows us to only check upto 25
	#accounts, we did the privacy note now just need to check if we can
	#increase the amount
	index = 0
	
	for current_account in my_accounts:
		if index == 25:
			break
		
		index = index + 1
		
		fields=[
			AdAccount.Field.account_id,
			AdAccount.Field.name
			]
		
		current_account.remote_read(fields=fields)
		
		if account_model.account_name == str(current_account[AdAccount.Field.name]):
			break
		
	ad_campaigns = current_account.get_ad_campaigns()
				
	for current_campaign in ad_campaigns:
		
		fields=[
			AdCampaign.Field.name,
    		AdCampaign.Field.status,
    		AdCampaign.Field.id]
			
		params = {
			'time_range': {
				'since': fbstartDate,
				'until': fbendDate,
			}
		}
			
		try:
			current_campaign.remote_read(fields=fields, params=params)
		except:
			pass
			
		fields = {    			
    		'impressions',
    		'clicks',
		'spend'
    	}
		try:
			data = str(current_campaign.get_insights(fields=fields,params=params))
		except:
			pass
		data = '['+data[12:]
		try:
			ast.literal_eval(data)
			json_string = json.dumps(data)
			parsed_data = json.loads(data)				
		except:
			continue
			
		campaign_model = FacebookCampaign()
		campaign_model.name = str(current_campaign[AdCampaign.Field.name])
		campaign_model.campaign_id = str(current_campaign[AdCampaign.Field.id])
		campaign_model.status = str(current_campaign[AdCampaign.Field.status])
		campaign_model.clicks = int(parsed_data[0]['clicks'])
		campaign_model.impressions = int(parsed_data[0]['impressions'])
		campaign_model.cost = float(parsed_data[0]['spend'])
		if not campaign_model.impressions == 0:
			campaign_model.CTR = round(campaign_model.clicks * 100/campaign_model.impressions,2)
			campaign_model.CPM = round(campaign_model.cost * 1000 / campaign_model.impressions,2)
		if not campaign_model.clicks == 0:
			campaign_model.CPC = round(campaign_model.cost/campaign_model.clicks,2)
		campaign_model.account = account_model
		campaign_model.save()	
 
def all_google_data(request, client_id):
	try:
		google_client = GoogleClient.objects.get(client_id=client_id)
	except ObjectDoesNotExist:
		return HttpResponse('The Client ID does not exist')
	adwords_client = adwords.AdWordsClient.LoadFromStorage()
	adwords_client.SetClientCustomerId(client_id)
	report_downloader = adwords_client.GetReportDownloader(version='v201506')  
  
	# Create report definition.
	report = {
		'reportName': 'CRITERIA_PERFORMANCE_REPORT',
		'dateRangeType': 'ALL_TIME',
		'reportType': 'CRITERIA_PERFORMANCE_REPORT',
		'downloadFormat': 'XML',
		'selector': {
			'fields': ['AccountDescriptiveName', 'AdGroupName', 'CampaignName',
						'Id', 'Criteria', 'Impressions', 'Clicks', 'Cost']
		}
	}
	file = open('output.xml', 'w')

	#creating the report downloader
	report_downloader.DownloadReport(
		report, file, skip_report_header=False, skip_column_header=False,
		skip_report_summary=False, include_zero_impressions=False)

	#save the file
	file.close()

	#parsing
	tree = ET.parse('output.xml')
	root = tree.getroot()

	#nested for loops to parse xml file
	for table in root.findall('table'):
		for row in table.findall('row'):
			
			#names are grabbed
			campaignName = row.get('campaign')
			adGroupName = row.get('adGroup')
			
			try:
				#does the campaign exist already
				campaign = GoogleCampaign.objects.get(campaign_name=campaignName)
			except ObjectDoesNotExist:
				#if not then make a new campaign
				campaign = GoogleCampaign()
				campaign.campaign_name = campaignName
				campaign.client = google_client
				campaign.save()
			
			try:
				#does the adgroup exist
				adGroup = GoogleAdGroup.objects.get(ad_group_name=adGroupName, campaign_name=campaignName)
			except ObjectDoesNotExist:
				#if not make a new
				adGroup = GoogleAdGroup()
				adGroup.ad_group_name = adGroupName                        
			
			#set the hierarchy of google data
			adGroup.campaign = campaign
			adGroup.campaign_name = campaignName
			adGroup.save()
			
			#create a new keyword for every entity
			data = GoogleKeyword()
			data.keyword_id = row.get('keywordID')
			data.keyword_placement = row.get('keywordPlacement')
			data.clicks = row.get('clicks')
			data.impressions = row.get('impressions')
			data.cost = row.get('cost')
			data.cost = str(float(data.cost)/1000000)
			data.adgroup = adGroup
			data.save()		

def all_fb_data(request, account_model):

	try:
		fb_acc = SocialAccount.objects.get(user_id = request.user.id,provider='facebook')
		fb_tok = SocialToken.objects.get(account=fb_acc)
	except:
		return HttpResponse("error connecting Social Accounts")
	
	#setting the user information
	my_app_id = '1604519246476149'
	my_app_secret = '5a93aee73f1d2856dd542f53e268e483'
	my_access_token = fb_tok.token
	
	#gets the ad accounts in a single, pre-existing facebook account
	FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
	me = objects.AdUser(fbid='me')
	my_accounts = list(me.get_ad_accounts())

	#does it have ad accounts
	if len(my_accounts) == 0:
		return HttpResponse("no Ad Accounts Exist")
	
	#important note, facebook allows us to only check upto 25
	#accounts, we did the privacy note now just need to check if we can
	#increase the amount
	index = 0
	
	for current_account in my_accounts:
		if index == 25:
			break
		
		index = index + 1
		
		fields=[
			AdAccount.Field.account_id,
			AdAccount.Field.name
			]
		
		current_account.remote_read(fields=fields)
		
		if account_model.account_name == str(current_account[AdAccount.Field.name]):
			break
		
	ad_campaigns = current_account.get_ad_campaigns()
	
	for current_campaign in ad_campaigns:
		
		fields=[
			AdCampaign.Field.name,
   			AdCampaign.Field.status,
   			AdCampaign.Field.id]
		try:
			current_campaign.remote_read(fields=fields)
		except:
			pass
			
		fields = {    			
   			'impressions',
   			'clicks',
		'spend'
   		}
		try:
			data = str(current_campaign.get_insights(fields=fields))
		except:
			pass
		data = '['+data[12:]
		try:
			ast.literal_eval(data)
			json_string = json.dumps(data)
			parsed_data = json.loads(data)				
		except:
			continue
			
		campaign_model = FacebookCampaign()
		campaign_model.name = str(current_campaign[AdCampaign.Field.name])
		campaign_model.campaign_id = str(current_campaign[AdCampaign.Field.id])
		campaign_model.status = str(current_campaign[AdCampaign.Field.status])
		campaign_model.clicks = int(parsed_data[0]['clicks'])
		campaign_model.impressions = int(parsed_data[0]['impressions'])
		campaign_model.cost = float(parsed_data[0]['spend'])
		if not campaign_model.impressions == 0:
			campaign_model.CTR = round(campaign_model.clicks * 100/campaign_model.impressions,2)
			campaign_model.CPM = round(campaign_model.cost * 1000 / campaign_model.impressions,2)
		if not campaign_model.clicks == 0:
			campaign_model.CPC = round(campaign_model.cost/campaign_model.clicks,2)
		campaign_model.account = account_model
		campaign_model.save()	

def month_google_data(request, client_id):
	
	try:
		google_client = GoogleClient.objects.get(client_id=client_id)
	except ObjectDoesNotExist:
		return HttpResponse('The Client ID does not exist')

	adwords_client = adwords.AdWordsClient.LoadFromStorage()
	adwords_client.SetClientCustomerId(client_id)
	report_downloader = adwords_client.GetReportDownloader(version='v201506')  
  
	# Create report definition.
	report = {
		'reportName': 'CRITERIA_PERFORMANCE_REPORT',
		'dateRangeType': 'LAST_30_DAYS',
		'reportType': 'CRITERIA_PERFORMANCE_REPORT',
		'downloadFormat': 'XML',
		'selector': {
			'fields': ['AccountDescriptiveName', 'AdGroupName', 'CampaignName',
						'Id', 'Criteria', 'Impressions', 'Clicks', 'Cost']
		}
	}
	file = open('output.xml', 'w')

	#creating the report downloader
	report_downloader.DownloadReport(
		report, file, skip_report_header=False, skip_column_header=False,
		skip_report_summary=False, include_zero_impressions=False)

	#save the file
	file.close()

	#parsing
	tree = ET.parse('output.xml')
	root = tree.getroot()

	#nested for loops to parse xml file
	for table in root.findall('table'):
		for row in table.findall('row'):
			
			#names are grabbed
			campaignName = row.get('campaign')
			adGroupName = row.get('adGroup')
			
			try:
				#does the campaign exist already
				campaign = GoogleCampaign.objects.get(campaign_name=campaignName)
			except ObjectDoesNotExist:
				#if not then make a new campaign
				campaign = GoogleCampaign()
				campaign.campaign_name = campaignName
				campaign.client = google_client
				campaign.save()
			
			try:
				#does the adgroup exist
				adGroup = GoogleAdGroup.objects.get(ad_group_name=adGroupName, campaign_name=campaignName)
			except ObjectDoesNotExist:
				#if not make a new
				adGroup = GoogleAdGroup()
				adGroup.ad_group_name = adGroupName                        
			
			#set the hierarchy of google data
			adGroup.campaign = campaign
			adGroup.campaign_name = campaignName
			adGroup.save()
			
			#create a new keyword for every entity
			data = GoogleKeyword()
			data.keyword_id = row.get('keywordID')
			data.keyword_placement = row.get('keywordPlacement')
			data.clicks = row.get('clicks')
			data.impressions = row.get('impressions')
			data.cost = row.get('cost')
			data.cost = str(float(data.cost)/1000000)
			data.adgroup = adGroup
			data.save()

def get_fb_accounts(request):	
	FacebookAccount.objects.all().delete()
	try:
		fb_acc = SocialAccount.objects.get(user_id = request.user.id,provider='facebook')
		fb_tok = SocialToken.objects.get(account=fb_acc)
	except:
		return HttpResponse("error connecting Social Accounts")
	
	#setting the user information
	my_app_id = '1604519246476149'
	my_app_secret = '5a93aee73f1d2856dd542f53e268e483'
	my_access_token = fb_tok.token
	
	#gets the ad accounts in a single, pre-existing facebook account
	FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
	me = objects.AdUser(fbid='me')
	my_accounts = list(me.get_ad_accounts())

	#does it have ad accounts
	if len(my_accounts) == 0:
		return HttpResponse("no Ad Accounts Exist")
	
	#important note, facebook allows us to only check upto 25
	#accounts, we did the privacy note now just need to check if we can
	#increase the amount
	index = 0
	
	for current_account in my_accounts:
		if index == 25:
			break
		
		index = index + 1
		
		fields=[
			AdAccount.Field.account_id,
			AdAccount.Field.name
			]
		
		current_account.remote_read(fields=fields)
		if AdAccount.Field.name == "":
			pass
		account_model = FacebookAccount()
		account_model.account_name = str(current_account[AdAccount.Field.name])
		account_model.account_id = str(current_account[AdAccount.Field.account_id])
		#account_model.report = report_model
		if not account_model.account_name == "":
			account_model.save()

def month_fb_data(request, account_model):

	try:
		fb_acc = SocialAccount.objects.get(user_id = request.user.id,provider='facebook')
		fb_tok = SocialToken.objects.get(account=fb_acc)
	except:
		return HttpResponse("error connecting Social Accounts")
	
	#setting the user information
	my_app_id = '1604519246476149'
	my_app_secret = '5a93aee73f1d2856dd542f53e268e483'
	my_access_token = fb_tok.token
	
	#gets the ad accounts in a single, pre-existing facebook account
	FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
	me = objects.AdUser(fbid='me')
	my_accounts = list(me.get_ad_accounts())

	#does it have ad accounts
	if len(my_accounts) == 0:
		return HttpResponse("no Ad Accounts Exist")
	
	#important note, facebook allows us to only check upto 25
	#accounts, we did the privacy note now just need to check if we can
	#increase the amount
	index = 0
	
	for current_account in my_accounts:
		if index == 25:
			break
		
		index = index + 1
		
		fields=[
			AdAccount.Field.account_id,
			AdAccount.Field.name
			]
		
		current_account.remote_read(fields=fields)
		
		if account_model.account_name == str(current_account[AdAccount.Field.name]):
			break
		
	ad_campaigns = current_account.get_ad_campaigns()
				
	for current_campaign in ad_campaigns:
		
		fields=[
			AdCampaign.Field.name,
    		AdCampaign.Field.status,
    		AdCampaign.Field.id]
				
		params = {
			'date_preset': 'last_30_days'
		}	
		
		try:
			current_campaign.remote_read(fields=fields, params=params)
		except:
			pass
			
		fields = {    			
    		'impressions',
    		'clicks',
		'spend'
    	}
		try:
			data = str(current_campaign.get_insights(fields=fields,params=params))
		except:
			pass
		data = '['+data[12:]
		try:
			ast.literal_eval(data)
			json_string = json.dumps(data)
			parsed_data = json.loads(data)				
		except:
			continue
			
		campaign_model = FacebookCampaign()
		campaign_model.name = str(current_campaign[AdCampaign.Field.name])
		campaign_model.campaign_id = str(current_campaign[AdCampaign.Field.id])
		campaign_model.status = str(current_campaign[AdCampaign.Field.status])
		campaign_model.clicks = int(parsed_data[0]['clicks'])
		campaign_model.impressions = int(parsed_data[0]['impressions'])
		campaign_model.cost = float(parsed_data[0]['spend'])
		if not campaign_model.impressions == 0:
			campaign_model.CTR = round(campaign_model.clicks * 100/campaign_model.impressions,2)
			campaign_model.CPM = round(campaign_model.cost * 1000 / campaign_model.impressions,2)
		if not campaign_model.clicks == 0:
			campaign_model.CPC = round(campaign_model.cost/campaign_model.clicks,2)
		campaign_model.account = account_model
		campaign_model.save()	
		
def index(request):
  try:
    fb_acc = SocialAccount.objects.get(user_id = request.user.id,provider='facebook')
    try:
      google_acc = SocialAccount.objects.get(user_id = request.user.id,provider='google')
      loginlist = [True,True]
    except ObjectDoesNotExist:
      loginlist = [True,False]
  except ObjectDoesNotExist:
    try:
      google_acc = SocialAccount.objects.get(user_id = request.user.id,provider='google')
      loginlist = [False,True]
    except ObjectDoesNotExist:
      loginlist = [False,False]

  return render(request, 'report/index.html', {'fb' : loginlist[0], 'google' : loginlist[1]})

def select(request, gcid=0, start_date=0, end_date=0):
	account_list = FacebookAccount.objects.all().order_by('account_name')
	report = Report.objects.get()
	if report.user == request.user.username:
		authenticated=True
	else:
		authenticated=False
	return render(request, 'report/select.html', {'account_list':account_list, 'authenticated':authenticated})


def grandview(request, gcid, fcid):
  report = Report.objects.get()
  #fb_src = Source.objects.get(name='Facebook')
  g_src = Source.objects.get(name='Google')
  fb_account = FacebookAccount.objects.get(pk=fcid)
  fb_adsource = adSource.objects.get(provider='Facebook', name=fb_account.account_name)
  campaign_list = FacebookCampaign.objects.filter(account=fb_account).order_by('name')
  g_adsource = adSource.objects.filter(provider='Google').order_by('name')
  if request.user.username == report.user:
    authenticated = True
  else:
    authenticated = False
  return render(request, 'report/grandview.html', {'authenticated':authenticated,'report':report, 'g_src': g_src, 'fb_account':fb_account, 'campaign_list':campaign_list, 'fb_adsource':fb_adsource, 'g_adsource':g_adsource})

def select_adgroup(request,gcampaign_id,fbacc_id):
  fbacc = FacebookAccount.objects.get(pk=fbacc_id)
  gcampaign = GoogleCampaign.objects.get(pk=gcampaign_id)
  adgroups =  gcampaign.googleadgroup_set.all()
  report = Report.objects.get()
  return render(request,  'report/adgroups.html', {'fbacc': fbacc, 'gcampaign': gcampaign, 'adgroups' : adgroups, 'report': report})

def show_results(request, gcampaign_id, fbacc_id, gadgroup_id):
  adgroup = GoogleAdGroup.objects.get(id=gadgroup_id)
  account = FacebookAccount.objects.get(id=fbacc_id)
  report = Report.objects.get()
  return render(request, 'report/results.html', {'adgroup': adgroup, 'account': account, 'report': report})

def adgroup(request, adgroup_id):
  adgroup = get_object_or_404(GoogleAdGroup,pk=adgroup_id)
  return render(request, 'report/adgroups.html', {'adgroup' : adgroup})


def campaigns(request):
  try:
    campaign_list = GoogleCampaign.objects.all()
    return render(request, 'report/campaigns.html', {'campaigns': campaign_list})
  except ObjectDoesNotExist:
    return HttpResponse("No Campaigns Exist")

def privacypolicy(request):
	return render(request, 'report/privacypolicy.html')


def result(request, campaign_id):
  campaign = get_object_or_404(GoogleCampaign, pk=campaign_id)
  return render(request, 'report/main.html',{'Campaign': campaign})
  
def getid(request,start_date,end_date):
  ccid_list = GoogleClient.objects.filter(user=request.user).order_by('client_name')
  get_fb_accounts(request)
  return render(request,'report/id.html',{'start_date': start_date, 'end_date': end_date, 'ccid_list':ccid_list})

def load(request,start_date,end_date,gcid,fcid):
	return render(request, 'report/load.html')
