# Generated by Django 5.1.5 on 2025-02-06 11:15

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('a_rtchat', '0008_rename_participants_chatroom_member_participant'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='chatroom_member',
            unique_together={('chatroom', 'participant')},
        ),
    ]
