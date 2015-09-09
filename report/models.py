from django.db import models
from datetime import datetime

class Account(models.Model):
    account_name = models.CharField(max_length=200,default='')
    customer_id = models.CharField(max_length=12,default = '000-000-0000')

    def __str__(self):
        return self.account_name

class Campaign(models.Model):
     campaign_name = models.CharField(max_length=200, default='')
     def __str__(self):
         return self.campaign_name
 
class AdGroup(models.Model):
     ad_group_name = models.CharField(max_length=200,default='')
     campaign_name = models.CharField(max_length=200,default='')
     campaign = models.ForeignKey(Campaign)
     def __str__(self):
         return self.ad_group_name
         
class Keyword(models.Model):
     keyword_id = models.BigIntegerField(default=0)
     keyword_placement = models.CharField(max_length=200,default='')
     clicks = models.BigIntegerField(default = 0)
     impressions = models.BigIntegerField(default = 0)
     cost = models.FloatField(default = 0.0)
     adgroup = models.ForeignKey(AdGroup)
     def __str__(self):
         return self.keyword_placement
