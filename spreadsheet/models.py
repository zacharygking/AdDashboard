from django.db import models

class Google(models.Model):
	clicks = models.IntegerField(default=0)
	impressions = models.IntegerField(default=0)
	cost = models.FloatField(default=0)
	
	def  __str__(self):
		return 'Google'
	
class Facebook(models.Model):	
	clicks = models.IntegerField(default=0)
	impressions = models.IntegerField(default=0)
	cost = models.FloatField(default=0)
	
	def __str__(self):
		return 'Facebook'
