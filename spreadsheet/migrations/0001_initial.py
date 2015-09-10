# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Facebook',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('clicks', models.IntegerField(default=0)),
                ('impressions', models.IntegerField(default=0)),
                ('cost', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Google',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('clicks', models.IntegerField(default=0)),
                ('impressions', models.IntegerField(default=0)),
                ('cost', models.FloatField(default=0)),
            ],
        ),
    ]
