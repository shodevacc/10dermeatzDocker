# Generated by Django 3.0.8 on 2020-08-07 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_deliveryaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryaddress',
            name='addInfo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
