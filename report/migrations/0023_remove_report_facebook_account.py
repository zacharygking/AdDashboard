# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0022_auto_20150918_0950'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='facebook_account',
        ),
    ]
