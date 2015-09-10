# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fb', '0003_auto_20150909_2037'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='account_cost',
            field=models.FloatField(default=0),
        ),
    ]
