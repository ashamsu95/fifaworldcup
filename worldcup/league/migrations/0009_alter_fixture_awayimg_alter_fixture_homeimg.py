# Generated by Django 4.1 on 2022-10-06 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0008_fixture_awayimg_fixture_homeimg_fixture_matchtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixture',
            name='awayimg',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='fixture',
            name='homeimg',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
