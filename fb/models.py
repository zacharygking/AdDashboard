from django.db import models

class Account(models.Model):
	account_id = models.CharField(max_length=200,default='')
	
	def __str__(self):
		return self.account_id
		
class Campaign(models.Model):
	name = models.CharField(max_length=200, default='')
	campaign_id = models.CharField(max_length=200, default='')
	status = models.CharField(max_length=200, default='')
	clicks = models.IntegerField(default=0)
	cpc = models.FloatField(default=0)
	impressions = models.IntegerField(default=0)
	account = models.ForeignKey(Account)
	
	def __str__(self):
		return self.name
