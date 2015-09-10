from django.db import models

class Metric(models.Model):
	name = models.CharField(max_length=200,default='')
	clicks = models.IntegerField(default=0)
	impressions = models.IntegerField(default=0)
	cost = models.FloatField(default=0)
	
	def  __str__(self):
		return self.name
