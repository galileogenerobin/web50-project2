# Generated by Django 4.0.3 on 2022-04-03 09:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_listing_watching'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='listing',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='listing',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
