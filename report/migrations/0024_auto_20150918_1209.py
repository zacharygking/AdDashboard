# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0023_remove_report_facebook_account'),
    ]

    operations = [
        migrations.RenameField(
            model_name='facebookcampaign',
            old_name='cpc',
            new_name='CPC',
        ),
        migrations.AddField(
            model_name='facebookcampaign',
            name='CPM',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='facebookcampaign',
            name='CTR',
            field=models.FloatField(default=0),
        ),
    ]
