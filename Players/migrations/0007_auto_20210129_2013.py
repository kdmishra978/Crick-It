# Generated by Django 3.1.3 on 2021-01-29 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Players', '0006_auto_20201222_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='image',
            field=models.ImageField(default='Players/default.jpg', upload_to='Players/'),
        ),
    ]
