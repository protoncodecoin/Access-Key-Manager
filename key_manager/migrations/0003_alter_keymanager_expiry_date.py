# Generated by Django 5.0.6 on 2024-06-20 21:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('key_manager', '0002_alter_keymanager_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keymanager',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 20, 21, 51, 28, 180822, tzinfo=datetime.timezone.utc)),
        ),
    ]