# Generated by Django 3.0.8 on 2020-07-28 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_products_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='category',
            field=models.CharField(choices=[('poultry', 'POULTRY'), ('mutton', 'MUTTON'), ('seafood', 'SEAFOOD')], default='ADD SOON', max_length=15),
        ),
        migrations.AlterField(
            model_name='products',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]