from django.shortcuts import render
from django.http import HttpResponse
from facebookads.api import FacebookAdsApi
from facebookads import objects
from facebookads.objects import AdAccount
from facebookads.objects import AdCampaign
from allauth.socialaccount.models import SocialToken, SocialAccount
import json
import ast
from fb.models import Account, Campaign

def index(request):
	return HttpResponse('jsung')

def get_report(request):
	
	Campaign.objects.all().delete()
	Account.objects.all().delete()
	
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
	index = 0
  	
	for current_account in my_accounts:
		if index == 5:
			break
		index = index + 1
		
		current_account.remote_read(fields=[
				AdAccount.Field.account_id,
		])
		
		account_model = Account()
		account_model.account_id = str(current_account[AdAccount.Field.account_id])
		account_model.save()
		
		try:
			ad_campaigns = current_account.get_ad_campaigns()
		except:
			continue
				
		for current_campaign in ad_campaigns:
		
			current_campaign.remote_read(fields=[
				AdCampaign.Field.name,
    			AdCampaign.Field.status,
    			AdCampaign.Field.id,
    		])
			fields = {
    			'impressions',
    			'clicks',
    			'cpc'
    		}
			data = str(current_campaign.get_insights(fields=fields))
			data = '['+data[12:]
			try:
				ast.literal_eval(data)
				json_string = json.dumps(data)
				parsed_data = json.loads(data)				
			except:
				continue
			
			campaign_model = Campaign()
			campaign_model.name = str(current_campaign[AdCampaign.Field.name])
			campaign_model.campaign_id = str(current_campaign[AdCampaign.Field.id])
			campaign_model.status = str(current_campaign[AdCampaign.Field.status])
			campaign_model.clicks = int(parsed_data[0]['clicks'])
			campaign_model.cpc = float(parsed_data[0]['cpc'])
			campaign_model.impressions = int(parsed_data[0]['impressions'])
			campaign_model.account = account_model
			campaign_model.save()
	
	return HttpResponse("success")
		
