from django.db import models
from datetime import datetime

class Report(models.Model):
	name = models.CharField(max_length=200, default='')
	customerID = models.CharField(max_length=12, default='')

	last_report_date = models.DateTimeField('date collected', default=datetime.now())
	clicks = models.IntegerField(default = 0)
	impressions = models.IntegerField(default = 0)
	cost = models.IntegerField(default = 0)


	def __str__(self):
		return self.name


