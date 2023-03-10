# Generated by Django 3.1.3 on 2021-01-06 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Teams', '0006_auto_20210103_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('venue', models.CharField(max_length=100)),
                ('number_of_teams', models.IntegerField()),
                ('overs', models.IntegerField()),
                ('auction_budget', models.IntegerField(default=100)),
                ('teams', models.ManyToManyField(null=True, related_name='teams', to='Teams.Team')),
            ],
        ),
    ]
