# Generated by Django 4.1 on 2022-09-21 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_myuser_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='phone',
            field=models.IntegerField(default=0),
        ),
    ]
