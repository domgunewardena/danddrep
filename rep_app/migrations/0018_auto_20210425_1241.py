# Generated by Django 3.1.3 on 2021-04-25 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rep_app', '0017_review_tagged'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='tagged',
            field=models.BooleanField(default=False, null=True),
        ),
    ]