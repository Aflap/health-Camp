# Generated by Django 4.2.7 on 2025-03-06 04:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('camp', '0009_patient_email_patient_school_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='patient_id',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='pdf_file',
            field=models.FileField(default=django.utils.timezone.now, upload_to='pdfs/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='camprequest',
            name='pdf_file',
            field=models.FileField(upload_to='pdfs/'),
        ),
    ]
