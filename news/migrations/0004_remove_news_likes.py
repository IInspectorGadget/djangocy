# Generated by Django 3.0.4 on 2020-03-18 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20200317_2153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='likes',
        ),
    ]