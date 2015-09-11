# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0012_auto_20150911_1824'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('account_name', models.CharField(max_length=200, default='')),
                ('account_id', models.CharField(max_length=200, default='')),
                ('account_cost', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='FacebookCampaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200, default='')),
                ('campaign_id', models.CharField(max_length=200, default='')),
                ('status', models.CharField(max_length=200, default='')),
                ('clicks', models.BigIntegerField(default=0)),
                ('cpc', models.FloatField(default=0)),
                ('impressions', models.BigIntegerField(default=0)),
                ('account', models.ForeignKey(to='report.FacebookAccount')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('date_taken', models.DateTimeField(auto_now_add=True)),
                ('user', models.CharField(max_length=200, default='')),
            ],
        ),
        migrations.AddField(
            model_name='facebookaccount',
            name='report',
            field=models.ForeignKey(blank=True, to='report.Report', null=True),
        ),
        migrations.AddField(
            model_name='googlecampaign',
            name='report',
            field=models.ForeignKey(blank=True, to='report.Report', null=True),
        ),
    ]
