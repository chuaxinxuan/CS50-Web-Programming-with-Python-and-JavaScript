# Generated by Django 3.2.15 on 2022-09-10 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_alter_auctionlisting_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='category',
            field=models.CharField(default='No category or Others', max_length=100),
        ),
    ]
