# Generated by Django 2.2.7 on 2020-05-13 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0020_auto_20200506_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='name',
            field=models.CharField(max_length=70),
        ),
    ]
