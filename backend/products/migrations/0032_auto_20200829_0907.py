# Generated by Django 3.1 on 2020-08-29 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0031_auto_20200823_0807'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CategoryImages', models.ImageField(upload_to='Category_Images')),
                ('category', models.CharField(choices=[('poultry', 'POULTRY'), ('mutton', 'MUTTON'), ('seafood', 'SEAFOOD')], default='ADD SOON', max_length=15)),
            ],
        ),
        migrations.AlterField(
            model_name='caoruselimages',
            name='CaoruselImage',
            field=models.ImageField(upload_to='Carousel_Images'),
        ),
        migrations.AlterField(
            model_name='products',
            name='img',
            field=models.ImageField(upload_to='Product_Images'),
        ),
    ]
