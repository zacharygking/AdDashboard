from django.shortcuts import render
from django.http import HttpResponse
from facebookads.api import FacebookAdsApi
from facebookads import objects
from facebookads.objects import AdAccount
from facebookads.objects import AdCampaign
from allauth.socialaccount.models import SocialToken, SocialAccount
import json
import ast

def index(request):
	return HttpResponse('jsung')

def get_report(request):

	#check if user is authenticated
	if not request.user.is_authenticated():
		return render(request, 'account/login.html')	

	#setting the user information
	my_app_id = '1604519246476149'
	my_app_secret = '5a93aee73f1d2856dd542f53e268e483'
	current_user = SocialAccount.objects.get(user=request.user)
	current_token = SocialToken.objects.get(account=current_user)
	my_access_token = current_token.token
  
	FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
	me = objects.AdUser(fbid='me')
	my_accounts = list(me.get_ad_accounts())
  
	if len(my_accounts) == 0:
		return HttpResponse("no Ad Accounts Exist")
  
	for current_account in my_accounts:
		ad_campaigns = current_account.get_ad_campaigns()
		if len(ad_campaigns) == 0:
			return HttpResponse("no Campaigns Exist")
		
		try:
			for current_campaign in ad_campaigns:
				current_campaign.remote_read(fields=[
					AdCampaign.Field.name,
	    			AdCampaign.Field.objective,
	    			AdCampaign.Field.status,
	    			AdCampaign.Field.id,
	    		])
				fields = {
	    			'account_id',
	    			'impressions',
	    			'clicks',
	    			'cpc'
	    		}
				print(current_campaign[AdCampaign.Field.name])
				data = str(current_campaign.get_insights(fields=fields))
				data = '['+data[12:]
				print(data)
				ast.literal_eval(data)
				json_string = json.dumps(data)
				parsed_data = json.loads(data)
				print(parsed_data[0]['clicks'])
		except:
