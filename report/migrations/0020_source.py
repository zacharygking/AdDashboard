# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0019_auto_20150917_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(default='', max_length=200)),
                ('clicks', models.IntegerField(default=0)),
                ('impressions', models.IntegerField(default=0)),
                ('cost', models.FloatField(default=0)),
            ],
        ),
    ]
