# Generated by Django 3.1 on 2020-08-14 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_orderitem_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='delivery_personelle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=25)),
            ],
        ),
    ]
