# Generated by Django 3.1 on 2020-08-23 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0030_auto_20200823_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
