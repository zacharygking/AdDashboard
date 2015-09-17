# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0014_auto_20150911_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='date_range',
            field=models.CharField(default='', max_length=200),
        ),
    ]
