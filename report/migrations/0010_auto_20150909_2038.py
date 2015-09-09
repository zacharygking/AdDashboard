# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0009_auto_20150828_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='clicks',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='impressions',
            field=models.BigIntegerField(default=0),
        ),
    ]
