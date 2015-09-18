# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0021_auto_20150917_1453'),
    ]

    operations = [
        migrations.CreateModel(
            name='adSource',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('provider', models.CharField(default='', max_length=200)),
                ('name', models.CharField(default='', max_length=200)),
                ('clicks', models.IntegerField(default=0)),
                ('impressions', models.IntegerField(default=0)),
                ('cost', models.FloatField(default=0)),
                ('CTR', models.FloatField(default=0)),
                ('CPC', models.FloatField(default=0)),
                ('CPM', models.FloatField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='report',
            name='facebook_account',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='report',
            name='google_account',
            field=models.CharField(default='', max_length=200),
        ),
    ]
