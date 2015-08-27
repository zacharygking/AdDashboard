from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse("Hello, world. You're at the report index.")

#!/usr/bin/python

#Google copyright

import logging
import sys
import xml.etree.ElementTree as ET
from googleads import adwords

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.transport').setLevel(logging.DEBUG)


def main(client):
  report_downloader = client.GetReportDownloader(version='v201506')

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

if __name__ == '__main__':
  adwords_client = adwords.AdWordsClient.LoadFromStorage()
  main(adwords_client)
  tree = ET.parse('output.xml')
  root = tree.getroot()

