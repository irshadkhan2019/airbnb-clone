# Generated by Django 2.2.5 on 2023-04-01 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20230401_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(blank=True, choices=[('english', 'English'), ('hindi', 'Hindi')], max_length=10, null=True),
        ),
    ]