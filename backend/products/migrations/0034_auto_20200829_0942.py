# Generated by Django 3.1 on 2020-08-29 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0033_categoryimages_categoryinfo'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CategoryImages',
            new_name='CategoryInfo',
        ),
    ]