# Generated by Django 3.1 on 2020-08-15 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_auto_20200815_1041'),
    ]

    operations = [
        migrations.RenameField(
            model_name='otp',
            old_name='user',
            new_name='username',
        ),
    ]
