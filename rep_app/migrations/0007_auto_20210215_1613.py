# Generated by Django 3.1.3 on 2021-02-15 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rep_app', '0006_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurant', models.CharField(max_length=30)),
                ('text', models.TextField(default='', max_length=1000)),
            ],
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
