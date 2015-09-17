# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0018_report_date_range'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='date_range',
            field=models.CharField(max_length=200, default=''),
        ),
    ]
