# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0004_auto_20150826_2055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='customerID',
        ),
        migrations.RemoveField(
            model_name='report',
            name='last_report_date',
        ),
        migrations.RemoveField(
            model_name='report',
            name='name',
        ),
        migrations.AddField(
            model_name='report',
            name='account_descriptive_name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='report',
            name='ad_group_name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='report',
            name='campaign_name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='report',
            name='criteria',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='report',
            name='id_number',
            field=models.IntegerField(default=0),
        ),
    ]
