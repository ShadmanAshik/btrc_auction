# Generated by Django 3.2.12 on 2022-03-23 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0007_alter_bidding_biddingtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='currentround',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
