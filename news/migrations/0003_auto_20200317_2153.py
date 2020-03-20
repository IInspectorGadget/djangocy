# Generated by Django 3.0.4 on 2020-03-17 18:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_remove_news_date_pub'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='date_pub',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]