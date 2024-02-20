from typing import final

from django.contrib.auth.models import AbstractUser
from django.db import models


@final
class Sura(models.Model):
    sura_id = models.IntegerField(primary_key=True)
    link = models.CharField(max_length=512)

    class Meta:
        db_table = 'suras'


@final
class City(models.Model):
    city_id = models.CharField(editable=False, primary_key=True)
    name = models.CharField(max_length=64)

    class Meta:
        db_table = 'cities'


@final
class File(models.Model):
    file_id = models.CharField(editable=False, primary_key=True)
    telegram_file_id = models.CharField(max_length=128, null=True)
    link = models.CharField(max_length=128, null=True)
    created_at = models.DateTimeField()
    filename = models.CharField(max_length=512, null=True)

    class Meta:
        db_table = 'files'


@final
class Ayat(models.Model):
    ayat_id = models.BigAutoField(primary_key=True)
    public_id = models.CharField(editable=False, unique=True)
    day = models.IntegerField(null=True)
    sura = models.ForeignKey(Sura, on_delete=models.PROTECT)
    audio = models.ForeignKey(File, on_delete=models.PROTECT)
    ayat_number = models.CharField(max_length=16)
    content = models.TextField()
    arab_text = models.TextField()
    transliteration = models.TextField()

    class Meta:
        db_table = 'ayats'


@final
class Message(models.Model):
    message_id = models.BigIntegerField(primary_key=True)
    message_json = models.JSONField()
    is_unknown = models.BooleanField()
    trigger_message_id = models.BigIntegerField()

    class Meta:
        db_table = 'messages'


@final
class User(AbstractUser):
    chat_id = models.BigIntegerField(primary_key=True)
    is_active = models.BooleanField()
    comment = models.CharField(max_length=128)
    day = models.IntegerField()
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    referrer_id = models.ForeignKey('self', on_delete=models.PROTECT, null=True)
    legacy_id = models.BigIntegerField()

    class Meta:
        db_table = 'users'


@final
class UserAction(models.Model):
    user_action_id = models.CharField(primary_key=True, editable=False)
    date_time = models.DateTimeField()
    action = models.CharField(max_length=16)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        db_table = 'user_actions'
