# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spreadsheet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(default='', max_length=200)),
                ('clicks', models.IntegerField(default=0)),
                ('impressions', models.IntegerField(default=0)),
                ('cost', models.FloatField(default=0)),
            ],
        ),
        migrations.DeleteModel(
            name='Facebook',
        ),
        migrations.DeleteModel(
            name='Google',
        ),
    ]
