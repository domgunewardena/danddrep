# Generated by Django 3.1.3 on 2021-03-23 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rep_app', '0013_auto_20210312_1645'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='tag',
            field=models.ManyToManyField(null=True, to='rep_app.Tag'),
        ),
    ]