# Generated by Django 4.2 on 2023-06-08 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_complaint_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='datetime',
            field=models.DateTimeField(default='2012-12-12 00:00:00'),
        ),
    ]
