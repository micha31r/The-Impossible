# Generated by Django 2.2.7 on 2020-07-13 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='description',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='short_description',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='question',
            name='description',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='question',
            name='short_description',
            field=models.CharField(max_length=150),
        ),
    ]