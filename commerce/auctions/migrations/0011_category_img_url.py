# Generated by Django 4.0.3 on 2022-04-04 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_listing_winning_bidder'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='img_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
