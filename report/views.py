#!/usr/bin/python

from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import logging
import sys
import xml.etree.ElementTree as ET
from googleads import adwords
from report.models import Account, Campaign, AdGroup, Keyword
from django.core.exceptions import ObjectDoesNotExist
from allauth.socialaccount.models import SocialToken, SocialAccount
from report.forms import DateForm

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



  response = "i_y = " + i_y + " i_d = " + i_d + " i_m = " + i_m + '<br>' + "f_y = " + f_y + " f_d = " + f_d + " f_m = " + f_m
  response = response + "<br><u> FACEBOOK TOKEN </u><br>" + fb_tok.token + "<u> GOOGLE TOKEN </u><br>" + google_tok.token
  return HttpResponse(response)

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


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)


def adgroup(request, adgroup_id):
  adgroup = get_object_or_404(AdGroup,pk=adgroup_id)
  return render(request, 'report/adgroups.html', {'adgroup' : adgroup})


def campaigns(request):
  try:
    campaign_list = Campaign.objects.all()
    return render(request, 'report/campaigns.html', {'campaigns': campaign_list})
  except ObjectDoesNotExist:
    return HttpResponse("No Campaigns Exist")


def result(request, campaign_id):
  campaign = get_object_or_404(Campaign, pk=campaign_id)
  return render(request, 'report/main.html',{'Campaign': campaign})


def main(request, time_id):
  Campaign.objects.all().delete()
  AdGroup.objects.all().delete()
  Keyword.objects.all().delete()
  adwords_client = adwords.AdWordsClient.LoadFromStorage()
  report_downloader = adwords_client.GetReportDownloader(version='v201506')
  
  time_id = int(time_id)

  if time_id == 1:
          date = 'LAST_7_DAYS'
  elif time_id == 2:
          date = 'THIS_MONTH'
  elif time_id == 3:
          date = 'ALL_TIME'
  else:
          return HttpResponse("time_id is not 1, 2, or 3")
  
  # Create report definition.
  report = {
      'reportName': date+'_CRITERIA_PERFORMANCE_REPORT',
      'dateRangeType': date,
      'reportType': 'CRITERIA_PERFORMANCE_REPORT',
      'downloadFormat': 'XML',
      'selector': {
          'fields': ['AccountDescriptiveName', 'AdGroupName', 'CampaignName',
                     'Id', 'Criteria', 'Impressions', 'Clicks', 'Cost']
      }
  }

  # You can provide a file object to write the output to. For this demonstration
  # we use sys.stdout to write the report to the screen.
  file = open('output.xml', 'w')

  report_downloader.DownloadReport(
      report, file, skip_report_header=False, skip_column_header=False,
      skip_report_summary=False, include_zero_impressions=False)

  file.close()

  tree = ET.parse('output.xml')
  root = tree.getroot()

  for table in root.findall('table'):
  	for row in table.findall('row'):
  		campaignName = row.get('campaign')
  		adGroupName = row.get('adGroup')
  		try:
                        campaign = Campaign.objects.get(campaign_name=campaignName)
  		except ObjectDoesNotExist:
                        campaign = Campaign()
                        campaign.campaign_name = campaignName
                        campaign.save()
  		try:
                        adGroup = AdGroup.objects.get(ad_group_name=adGroupName, campaign_name=campaignName)
  		except ObjectDoesNotExist:
                        adGroup = AdGroup()
                        adGroup.ad_group_name = adGroupName                        
                         
  		adGroup.campaign = campaign
  		adGroup.campaign_name = campaignName
  		adGroup.save()
  		
  		data = Keyword()
  		data.keyword_id = row.get('keywordID')
  		data.keyword_placement = row.get('keywordPlacement')
  		data.clicks = row.get('clicks')
  		data.impressions = row.get('impressions')
  		data.cost = row.get('cost')
  		data.cost = str(float(data.cost)/1000000)
  		data.adgroup = adGroup
  		data.save()

  return campaigns(request)
