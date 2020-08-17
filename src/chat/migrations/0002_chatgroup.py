# Generated by Django 2.2.7 on 2020-08-08 00:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True)),
                ('key', models.SlugField(blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('member', models.ManyToManyField(blank=True, related_name='member', to=settings.AUTH_USER_MODEL)),
                ('message', models.ManyToManyField(blank=True, related_name='messages', to='chat.ChatMessage')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]