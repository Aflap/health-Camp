# Generated by Django 4.2.7 on 2025-03-05 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camp', '0006_medicalcenter_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalcenter',
            name='password',
            field=models.CharField(max_length=255),
        ),
    ]
