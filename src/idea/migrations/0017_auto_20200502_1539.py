# Generated by Django 2.2.7 on 2020-05-02 03:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0016_idea_header_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='header_img',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userupload.File'),
        ),
    ]
