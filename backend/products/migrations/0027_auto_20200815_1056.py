# Generated by Django 3.1 on 2020-08-15 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0026_auto_20200815_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='otp',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]