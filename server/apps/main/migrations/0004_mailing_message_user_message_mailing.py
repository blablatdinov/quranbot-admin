# Generated by Django 4.2.10 on 2024-03-03 18:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0003_message_trigger_callback_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('mailing_id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'mailings',
            },
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
                null=True,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='mailing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.mailing', null=True),
            preserve_default=False,
        ),
    ]