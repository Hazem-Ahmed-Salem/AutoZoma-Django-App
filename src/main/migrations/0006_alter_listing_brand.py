# Generated by Django 5.0.6 on 2024-08-02 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_listing_brand_likedlisting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='brand',
            field=models.CharField(choices=[('bmw', 'BMW'), ('mercedes benz', 'Mercedes Benz'), ('audi', 'Audi'), ('subaru', 'Subaru'), ('tesla', 'Tesla'), ('jaguar', 'Jaguar'), ('land rover', 'Land Rover'), ('bentley', 'Bentley'), ('bugatti', 'Bugatti'), ('ferrari', 'Ferrari'), ('lamborghini', 'Lamborghini'), ('honda', 'Honda'), ('toyota', 'Toyota'), ('chevrolet', 'Chevrolet'), ('porsche', 'Porsche'), ('volvo', 'Volvo'), ('dodge', 'Dodge'), ('lotus', 'Lotus'), ('ford', 'Ford')], default=None, max_length=30),
        ),
    ]
