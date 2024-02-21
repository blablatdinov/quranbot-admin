# Generated by Django 4.2.10 on 2024-02-21 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='day',
            field=models.IntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='legacy_id',
            field=models.BigIntegerField(null=True),
        ),
    ]
