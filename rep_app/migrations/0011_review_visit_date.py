# Generated by Django 3.1.3 on 2021-03-12 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rep_app', '0010_auto_20210311_0816'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='visit_date',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
