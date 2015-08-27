from django.db import models
from datetime import datetime

class Report(models.Model):
    account_descriptive_name = models.CharField(max_length=200, default='')
    ad_group_name = models.CharField(max_length=200, default='')
    campaign_name = models.CharField(max_length=200, default = '')
    id_number = models.IntegerField(default=0)
    criteria = models.CharField(max_length=200,default='')
    clicks = models.IntegerField(default = 0)
    impressions = models.IntegerField(default = 0)
    cost = models.IntegerField(default = 0)

    def __str__(self):
        return self.campaign_name


