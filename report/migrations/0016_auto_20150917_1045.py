# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('report', '0015_report_date_range'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleClient',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('client_id', models.CharField(default='', max_length=200)),
                ('client_name', models.CharField(default='', max_length=200)),
                ('user', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='googlecampaign',
            name='report',
        ),
    ]
