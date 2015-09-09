# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0010_auto_20150909_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='keyword_id',
            field=models.BigIntegerField(default=0),
        ),
    ]
