# Generated by Django 3.1.3 on 2021-04-25 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rep_app', '0016_auto_20210326_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='tagged',
            field=models.BooleanField(default=False),
        ),
    ]