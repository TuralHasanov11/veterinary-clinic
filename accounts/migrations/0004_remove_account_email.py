# Generated by Django 4.0.1 on 2022-01-25 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_account_phone_alter_account_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='email',
        ),
    ]
