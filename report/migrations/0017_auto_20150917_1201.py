# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0016_auto_20150917_1045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='date_range',
        ),
        migrations.AddField(
            model_name='googlecampaign',
            name='client',
            field=models.ForeignKey(blank=True, null=True, to='report.GoogleClient'),
        ),
    ]
