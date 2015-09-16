#!/usr/bin/python

#import for all
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from report.models import Report, GoogleCampaign, GoogleAdGroup, GoogleKeyword, FacebookCampaign, FacebookAccount

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

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.transport').setLevel(logging.DEBUG)

def collect(request,start_date,end_date):

	i_y = start_date[0] + start_date[1] + start_date[2] + start_date[3]
	i_m = start_date[5] + start_date[6]
	i_d = start_date[8] + start_date[9]

	f_y = end_date[0] + end_date[1] + end_date[2] + end_date[3]
	f_m = end_date[5] + end_date[6]
	f_d = end_date[8] + end_date[9]

	try:
		fb_acc = SocialAccount.objects.get(user_id = request.user.id,provider='facebook')
		google_acc = SocialAccount.objects.get(user_id = request.user.id,provider='google')
		fb_tok = SocialToken.objects.get(account=fb_acc)
		google_tok = SocialToken.objects.get(account=google_acc)
	except:
		return HttpResponse("error connecting Social Accounts")
	
	#clear the database
	GoogleCampaign.objects.all().delete()
	GoogleAdGroup.objects.all().delete()
	GoogleKeyword.objects.all().delete()
	FacebookCampaign.objects.all().delete()
	FacebookAccount.objects.all().delete()
	Report.objects.all().delete()
		
	report_model = Report()
	report_model.user = request.user.username
	report_model.date_taken = datetime.now()
	report_model.save()
	
	googstartDate = i_y+i_m+i_d
	googendDate = f_y+f_m+f_d
	
	fbstartDate = i_y + '-' + i_m + '-' + i_d
	fbendDate = f_y + '-' + f_m + '-' + f_d
	
	#get the google data
	google_data(request, report_model, googstartDate, googendDate)
	
	#get the facebook data
	fb_data(request, report_model, fb_tok, fbstartDate, fbendDate)
	return HttpResponse('I cant believe its not butter')

'''
	method will create a report downloader implemented by google 
	and fetch the data which will then be stored in a xml file 
	and the xml file will be parsed to store it on django server
'''
def google_data(request, report_model, startDate, endDate):  
	adwords_client = adwords.AdWordsClient.LoadFromStorage()
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
				campaign.report = report_model
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
def fb_data(request, report_model, fb_tok, fbstartDate, fbendDate):	

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
	
	#!!!!important note, facebook allows us to only check upto 5
	#accounts, need to update policy statement
	index = 0
  	
	for current_account in my_accounts:
		if index == 5:
			break
		
		index = index + 1
		
		fields=[
			AdAccount.Field.account_id,
			AdAccount.Field.name
			]
		
		current_account.remote_read(fields=fields)
		
		account_model = FacebookAccount()
		account_model.account_name = str(current_account[AdAccount.Field.name])
		account_model.account_id = str(current_account[AdAccount.Field.account_id])
		account_model.report = report_model
		account_model.save()
		
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
		
			current_campaign.remote_read(fields=fields,params=params)
			
			fields = {    			
    			'impressions',
    			'clicks',
    			'cpc',
				'spend'
    		}
			data = str(current_campaign.get_insights(fields=fields,params=params))
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
			campaign_model.cpc = float(parsed_data[0]['cpc'])
			campaign_model.impressions = int(parsed_data[0]['impressions'])
			campaign_model.cost = float(parsed_data[0]['spend'])
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

def select(request):
  report = Report.objects.get(user=request.user.username)
  return render(request, 'report/select.html', {'Report': report})

def select_adgroup(request,gcampaign_id,fbacc_id):
  fbacc = FacebookAccount.objects.get(pk=fbacc_id)
  gcampaign = GoogleCampaign.objects.get(pk=gcampaign_id)
  adgroups =  gcampaign.googleadgroup_set.all()
  return render(request,  'report/adgroups.html', {'fbacc': fbacc, 'gcampaign': gcampaign, 'adgroups' : adgroups})

def adgroup(request, adgroup_id):
  adgroup = get_object_or_404(GoogleAdGroup,pk=adgroup_id)
  return render(request, 'report/adgroups.html', {'adgroup' : adgroup})


def campaigns(request):
  try:
    campaign_list = GoogleCampaign.objects.all()
    return render(request, 'report/campaigns.html', {'campaigns': campaign_list})
  except ObjectDoesNotExist:
    return HttpResponse("No Campaigns Exist")


def result(request, campaign_id):
  campaign = get_object_or_404(GoogleCampaign, pk=campaign_id)
  return render(request, 'report/main.html',{'Campaign': campaign})
