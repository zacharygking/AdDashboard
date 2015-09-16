# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0013_auto_20150911_1950'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facebookaccount',
            name='account_cost',
        ),
        migrations.AddField(
            model_name='facebookcampaign',
            name='cost',
            field=models.FloatField(default=0),
        ),
    ]
