# Generated by Django 5.0.6 on 2024-07-07 01:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_listing_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='transmisson',
            new_name='transmission',
        ),
    ]
