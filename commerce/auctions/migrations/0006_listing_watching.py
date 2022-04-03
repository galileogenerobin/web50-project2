# Generated by Django 4.0.3 on 2022-04-03 03:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_listing_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watching',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
