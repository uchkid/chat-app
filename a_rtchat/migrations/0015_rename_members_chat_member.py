# Generated by Django 5.1.5 on 2025-02-08 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('a_rtchat', '0014_alter_chat_created_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='members',
            new_name='member',
        ),
    ]
