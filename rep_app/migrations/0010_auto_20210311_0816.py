# Generated by Django 3.1.3 on 2021-03-11 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rep_app', '0009_auto_20210311_0641'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='manager',
        ),
        migrations.AddField(
            model_name='restaurant',
            name='manager',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='rep_app.manager'),
        ),
    ]