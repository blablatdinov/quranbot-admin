# Generated by Django 4.2.10 on 2024-03-06 13:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0004_mailing_message_user_message_mailing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='user',
        ),
        migrations.AddField(
            model_name='message',
            name='from_id',
            field=models.BigIntegerField(null=True),
        ),
    ]
