# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0006_auto_20150827_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='adgroup',
            name='campaign_name',
            field=models.CharField(default='', max_length=200),
        ),
    ]
