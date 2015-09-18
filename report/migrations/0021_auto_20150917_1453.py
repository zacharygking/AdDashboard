# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0020_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='CPC',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='source',
            name='CPM',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='source',
            name='CTR',
            field=models.FloatField(default=0),
        ),
    ]
