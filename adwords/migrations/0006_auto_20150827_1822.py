# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0005_auto_20150827_1750'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('ad_group_name', models.CharField(max_length=200, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('campaign_name', models.CharField(max_length=200, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('keyword_id', models.IntegerField(default=0)),
                ('keyword_placement', models.CharField(max_length=200, default='')),
                ('clicks', models.IntegerField(default=0)),
                ('impressions', models.IntegerField(default=0)),
                ('cost', models.IntegerField(default=0)),
                ('adgroup', models.ForeignKey(to='report.AdGroup')),
            ],
        ),
        migrations.DeleteModel(
            name='Report',
        ),
        migrations.AddField(
            model_name='adgroup',
            name='campaign',
            field=models.ForeignKey(to='report.Campaign'),
        ),
    ]
