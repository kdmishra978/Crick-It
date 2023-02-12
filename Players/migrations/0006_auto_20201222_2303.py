# Generated by Django 3.1.3 on 2020-12-22 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Players', '0005_auto_20201222_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='innings',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='runs',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='wickets',
            field=models.IntegerField(default=0),
        ),
    ]