# Generated by Django 4.2 on 2023-06-01 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_remove_complaint_name_complaint_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='photo',
            field=models.ImageField(upload_to='dashboard'),
        ),
    ]
