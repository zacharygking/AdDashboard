# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fb', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='accid',
            new_name='account_id',
        ),
        migrations.RenameField(
            model_name='campaign',
            old_name='camid',
            new_name='campaign_id',
        ),
        migrations.AddField(
            model_name='account',
            name='account_name',
            field=models.CharField(default='', max_length=200),
        ),
    ]
