# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0017_auto_20150917_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='date_range',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 19, 8, 51, 406165, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
