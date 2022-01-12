# Generated by Django 3.2.9 on 2022-01-05 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0003_auto_20211217_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='our_price',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='price',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='quantity',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='single_quantity',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='medicinecompany',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]