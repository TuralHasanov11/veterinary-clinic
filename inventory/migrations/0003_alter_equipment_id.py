# Generated by Django 3.2.9 on 2021-11-26 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20211119_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
