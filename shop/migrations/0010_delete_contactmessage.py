# Generated by Django 5.1 on 2024-09-24 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_rename_full_name_contactmessage_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Contactmessage',
        ),
    ]