# Generated by Django 4.0.3 on 2022-04-02 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listing_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='status',
            field=models.CharField(choices=[('Closed', 'Closed'), ('Active', 'Active')], default='Active', max_length=64),
        ),
    ]
