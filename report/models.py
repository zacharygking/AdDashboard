from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Report(models.Model):
	date_taken = models.DateTimeField(auto_now_add=True, blank=True)
	date_range = models.CharField(max_length=200, default='')
	user = models.CharField(max_length=200,default='')
	
	def __str__(self):
		return self.user
		
class Source(models.Model):
	name = models.CharField(max_length=200,default='')
	clicks = models.IntegerField(default=0)
	impressions = models.IntegerField(default=0)
	cost = models.FloatField(default=0)
	CTR = models.FloatField(default=0)
	CPC = models.FloatField(default=0)
	CPM = models.FloatField(default=0)
	
	def  __str__(self):
		return self.name
		
class adSource(models.Model):
	provider = models.CharField(max_length=200,default='')
	name = models.CharField(max_length=200,default='')
	clicks = models.IntegerField(default=0)
	impressions = models.IntegerField(default=0)
	cost = models.FloatField(default=0)
	CTR = models.FloatField(default=0)
	CPC = models.FloatField(default=0)
	CPM = models.FloatField(default=0)
	
	def  __str__(self):
		return self.name
		
class GoogleClient(models.Model):
	client_id = models.CharField(max_length=200, default='')
	client_name = models.CharField(max_length=200, default='')
	user = models.ForeignKey(User, blank=True, null=True)
	
	def __str__(self):
		return self.client_name	
	
class GoogleCampaign(models.Model):
	campaign_name = models.CharField(max_length=200, default='')
	client = models.ForeignKey(GoogleClient, blank=True, null=True)
    
	def __str__(self):
		return self.campaign_name
		
class GoogleAdGroup(models.Model):
    ad_group_name = models.CharField(max_length=200,default='')
    campaign_name = models.CharField(max_length=200,default='')
    campaign = models.ForeignKey(GoogleCampaign)
	
    def __str__(self):
        return self.ad_group_name
         
class GoogleKeyword(models.Model):
    keyword_id = models.BigIntegerField(default=0)
    keyword_placement = models.CharField(max_length=200,default='')
    clicks = models.BigIntegerField(default = 0)
    impressions = models.BigIntegerField(default = 0)
    cost = models.FloatField(default = 0.0)
    adgroup = models.ForeignKey(GoogleAdGroup)
	
    def __str__(self):
        return self.keyword_placement
		 
class FacebookAccount(models.Model):
	account_name = models.CharField(max_length=200, default='')
	account_id = models.CharField(max_length=200,default='')
	report = models.ForeignKey(Report, blank=True, null=True)
	
	def __str__(self):
		return self.account_name
		
class FacebookCampaign(models.Model):
	name = models.CharField(max_length=200, default='')
	campaign_id = models.CharField(max_length=200, default='')
	status = models.CharField(max_length=200, default='')
	clicks = models.BigIntegerField(default=0)
	cpc = models.FloatField(default=0)
	cost = models.FloatField(default=0)
	impressions = models.BigIntegerField(default=0)
	account = models.ForeignKey(FacebookAccount)
	
	def __str__(self):
		return self.name
