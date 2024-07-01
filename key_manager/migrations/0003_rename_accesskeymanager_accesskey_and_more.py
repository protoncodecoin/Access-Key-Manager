# Generated by Django 5.0.6 on 2024-07-01 22:23

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('key_manager', '0002_alter_accesskeymanager_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AccessKeyManager',
            new_name='AccessKey',
        ),
        migrations.RenameIndex(
            model_name='accesskey',
            new_name='key_manager_status_4870ce_idx',
            old_name='key_manager_status_b25b65_idx',
        ),
    ]
