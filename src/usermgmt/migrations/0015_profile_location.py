# Generated by Django 2.2.7 on 2020-06-21 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermgmt', '0014_auto_20200620_0409'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
