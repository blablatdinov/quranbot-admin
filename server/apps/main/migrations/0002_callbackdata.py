# Generated by Django 4.2.10 on 2024-03-02 03:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallbackData',
            fields=[
                ('callback_id', models.BigIntegerField(editable=False, primary_key=True, serialize=False)),
                ('date_time', models.DateTimeField()),
                ('json', models.JSONField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
