# Generated by Django 3.1.3 on 2021-03-04 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Players', '0008_auto_20210201_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]
