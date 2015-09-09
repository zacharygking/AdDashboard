# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fb', '0002_auto_20150904_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='clicks',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='impressions',
            field=models.BigIntegerField(default=0),
        ),
    ]
