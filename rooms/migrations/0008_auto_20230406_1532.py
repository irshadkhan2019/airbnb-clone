# Generated by Django 2.2.5 on 2023-04-06 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0007_auto_20230404_0949'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='bathrooms',
            new_name='bedrooms',
        ),
    ]
