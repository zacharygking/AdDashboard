#!/usr/bin/python

from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import logging
import sys
import xml.etree.ElementTree as ET
from googleads import adwords
from adwords.models import Account, Campaign, AdGroup, Keyword
from django.core.exceptions import ObjectDoesNotExist

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.transport').setLevel(logging.DEBUG)


def index(request):
	return render(request, 'adwords/index.html')


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)


def adgroup(request, adgroup_id):
  adgroup = get_object_or_404(AdGroup,pk=adgroup_id)
  return render(request, 'adwords/adgroups.html', {'adgroup' : adgroup})


def campaigns(request):
  try:
    campaign_list = Campaign.objects.all()
    return render(request, 'adwords/campaigns.html', {'campaigns': campaign_list})
  except ObjectDoesNotExist:
    return HttpResponse("No Campaigns Exist")


def result(request, campaign_id):
  campaign = get_object_or_404(Campaign, pk=campaign_id)
  return render(request, 'adwords/main.html',{'Campaign': campaign})


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
          return HTTPResponse("time_id is not 1, 2, or 3")
  
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
