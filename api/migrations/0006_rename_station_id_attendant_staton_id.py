# Generated by Django 4.2.2 on 2023-07-06 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_date_of_borth_attendant_date_of_birth'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendant',
            old_name='station_id',
            new_name='staton_id',
        ),
    ]