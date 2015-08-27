from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

def index(request):
	return HttpResponse("Hello, world. You're at the report index.")

#!/usr/bin/python

#Google copyright

import logging
import sys
import xml.etree.ElementTree as ET
from googleads import adwords
from report.models import Account, Campaign, AdGroup, Keyword

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.transport').setLevel(logging.DEBUG)

def result(request, campaign_id):
  campaign = get_object_or_404(Campaign, pk=campaign_id)
  return render(request, 'report/main.html',{'Campaign': campaign})


def main(request):
  adwords_client = adwords.AdWordsClient.LoadFromStorage()
  report_downloader = adwords_client.GetReportDownloader(version='v201506')

  # Create report definition.
  report = {
      'reportName': 'ALL_TIME_CRITERIA_PERFORMANCE_REPORT',
      'dateRangeType': 'ALL_TIME',
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
  		try:
  			campaign = Campaign.objects.get(campaign_name=campaignName)
  		except RuntimeError: 
  			campaign = Campaign()
  			campaign.campaign_name = campaignName
  			campaign.save()
  			
  			adGroupName = row.get('adGroup')
  		try:
  			adGroup = campaign.get(ad_group_name=adGroupName)
  		except RuntimeError:
  			adGroup = adGroup()
  			adGroup.ad_group_name = adGroupName
  			adGroup.save()
  			campaign.adGroup = adGroup
  			campaign.save()
  			
  		data = Keyword()
  		data.keyword_id = row.get('keywordID')
  		data.keyword_placement = row.get('keywordPlacement')
  		data.clicks = row.get('clicks')
  		data.impressions = row.get('impressions')
  		data.cost = row.get('cost')
  		data.save()
  		
  		campaign.adGroup.keyword = data

  return HttpResponse("done")
