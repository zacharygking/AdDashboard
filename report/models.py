from django.db import models
from datetime import datetime

class Campaign(models.Model):
    campaign_name = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.campaign_name

class AdGroup(models.Model):
    ad_group_name = models.CharField(max_length=200,default='')
    campaign = models.ForeignKey(Campaign)
    def __str__(self):
        return self.ad_group_name

class Keyword(models.Model):
    keyword_id = models.IntegerField(default=0)
    keyword_placement = models.CharField(max_length=200,default='')
    clicks = models.IntegerField(default = 0)
    impressions = models.IntegerField(default = 0)
    cost = models.IntegerField(default = 0)
    adgroup = models.ForeignKey(AdGroup)
    def __str__(self):
        return self.keyword_placement



