# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0011_auto_20150909_2038'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleAdGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('ad_group_name', models.CharField(max_length=200, default='')),
                ('campaign_name', models.CharField(max_length=200, default='')),
            ],
        ),
        migrations.RenameModel(
            old_name='Campaign',
            new_name='GoogleCampaign',
        ),
        migrations.RenameModel(
            old_name='Keyword',
            new_name='GoogleKeyword',
        ),
        migrations.DeleteModel(
            name='Account',
        ),
        migrations.RemoveField(
            model_name='adgroup',
            name='campaign',
        ),
        migrations.AlterField(
            model_name='googlekeyword',
            name='adgroup',
            field=models.ForeignKey(to='report.GoogleAdGroup'),
        ),
        migrations.DeleteModel(
            name='AdGroup',
        ),
        migrations.AddField(
            model_name='googleadgroup',
            name='campaign',
            field=models.ForeignKey(to='report.GoogleCampaign'),
        ),
    ]
