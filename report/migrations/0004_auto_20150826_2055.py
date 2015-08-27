# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0003_auto_20150826_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='clicks',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='impressions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='last_report_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 26, 20, 54, 59, 976203), verbose_name='date collected'),
        ),
    ]
