# Generated by Django 3.1.3 on 2021-02-01 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Players', '0007_auto_20210129_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='bataggression',
            field=models.CharField(choices=[('super', 'Super'), ('high', 'High'), ('normal', 'Normal'), ('low', 'Low')], default='normal', max_length=10),
        ),
        migrations.AddField(
            model_name='player',
            name='bowlaggression',
            field=models.CharField(choices=[('super', 'Super'), ('high', 'High'), ('normal', 'Normal'), ('low', 'Low')], default='normal', max_length=10),
        ),
    ]
