# Generated by Django 3.2.9 on 2022-01-05 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0005_auto_20220105_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='company',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='medicines.medicinecompany'),
        ),
    ]
