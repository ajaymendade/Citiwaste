# Generated by Django 4.2 on 2023-06-08 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_complaint_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='datetime',
            field=models.DateTimeField(default='2023-06-08 15:30:00'),
        ),
    ]