# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('accid', models.CharField(max_length=200, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200, default='')),
                ('camid', models.CharField(max_length=200, default='')),
                ('status', models.CharField(max_length=200, default='')),
                ('clicks', models.IntegerField(default=0)),
                ('cpc', models.FloatField(default=0)),
                ('impressions', models.IntegerField(default=0)),
                ('account', models.ForeignKey(to='fb.Account')),
            ],
        ),
    ]
