# Generated by Django 3.2.15 on 2022-09-10 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auctionlisting_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='winner',
            field=models.CharField(max_length=100, null=True),
        ),
    ]