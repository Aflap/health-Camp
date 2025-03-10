# Generated by Django 4.2.7 on 2025-03-04 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('camp', '0004_camprequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(default='Pending', max_length=20)),
                ('medical_center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='camp.medicalcenter')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='camp.school')),
            ],
        ),
    ]
