# Generated by Django 3.1 on 2020-08-12 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_auto_20200812_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
