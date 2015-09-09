# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0002_report_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='report',
            name='customerID',
            field=models.CharField(max_length=12, default=''),
        ),
    ]
