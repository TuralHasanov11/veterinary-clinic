# Generated by Django 3.2.9 on 2022-01-19 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MedicineCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=191, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=191, unique=True)),
                ('single_quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('price', models.FloatField(blank=True, default=0, null=True)),
                ('our_price', models.FloatField(blank=True, default=0, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='medicines.medicinecompany')),
            ],
        ),
    ]