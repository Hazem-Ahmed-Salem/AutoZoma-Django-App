# Generated by Django 5.0.6 on 2024-07-02 01:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_location_state_location_zip_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.location'),
        ),
    ]
