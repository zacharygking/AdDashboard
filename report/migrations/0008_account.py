# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0007_adgroup_campaign_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('account_name', models.CharField(default='', max_length=200)),
                ('customer_id', models.CharField(default='000-000-0000', max_length=12)),
            ],
        ),
    ]
