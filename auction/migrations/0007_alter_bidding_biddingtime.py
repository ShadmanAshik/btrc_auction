# Generated by Django 3.2.12 on 2022-03-23 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0006_round_biddingprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidding',
            name='biddingTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
