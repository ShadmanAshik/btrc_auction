# Generated by Django 3.2.12 on 2022-03-23 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0008_currentround_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentround',
            name='round',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
