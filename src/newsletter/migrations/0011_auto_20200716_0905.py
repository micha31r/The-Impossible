# Generated by Django 2.2.7 on 2020-07-16 09:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0010_auto_20200716_0804'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='slug',
            field=models.SlugField(default='MB6P7YCBPN108F0AOXII'),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='frequency',
            field=models.IntegerField(choices=[(1, 'Never'), (2, 'Weekly'), (3, 'Monthly')], default=2),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='last_sent',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 16, 9, 5, 43, 691146)),
        ),
    ]
