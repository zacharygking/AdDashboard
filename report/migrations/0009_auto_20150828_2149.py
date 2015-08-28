# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0008_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='cost',
            field=models.FloatField(default=0.0),
        ),
    ]
