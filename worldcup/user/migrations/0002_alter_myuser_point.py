# Generated by Django 4.1 on 2022-09-18 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='point',
            field=models.IntegerField(blank=True),
        ),
    ]
