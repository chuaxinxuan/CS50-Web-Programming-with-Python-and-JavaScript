# Generated by Django 3.2.15 on 2022-09-04 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_watchlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='listingid',
            new_name='listing',
        ),
    ]
