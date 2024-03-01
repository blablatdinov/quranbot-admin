"""Модели БД."""

from typing import ClassVar, final

from django.contrib.auth.models import AbstractUser
from django.db import models


@final
class Sura(models.Model):
    """Сура."""

    sura_id = models.IntegerField(primary_key=True)
    link = models.CharField(max_length=512)

    class Meta:
        db_table = 'suras'

    def __str__(self) -> str:
        """Строковое представление."""
        return 'Sura {0}'.format(self.sura_id)


@final
class City(models.Model):
    """Город."""

    city_id = models.CharField(editable=False, primary_key=True)
    name = models.CharField(max_length=64)

    class Meta:
        db_table = 'cities'

    def __str__(self) -> str:
        """Строковое представление."""
        return 'City "{0}"'.format(self.name)


@final
class File(models.Model):
    """Файл."""

    file_id = models.CharField(editable=False, primary_key=True)
    telegram_file_id = models.CharField(max_length=128, null=True)  # noqa: DJ001
    link = models.CharField(max_length=128, null=True)  # noqa: DJ001
    created_at = models.DateTimeField()
    filename = models.CharField(max_length=512, null=True)  # noqa: DJ001

    class Meta:
        db_table = 'files'

    def __str__(self) -> str:
        """Строковое представление."""
        return 'File "{0}"'.format(self.filename)


@final
class Ayat(models.Model):
    """Аят."""

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

    def __str__(self) -> str:
        """Строковое представление."""
        return 'Ayat {0}:{1}'.format(self.sura_id, self.ayat_number)


@final
class Message(models.Model):
    """Сообщение."""

    message_id = models.BigIntegerField(primary_key=True)
    message_json = models.JSONField()
    is_unknown = models.BooleanField()
    trigger_message_id = models.BigIntegerField(null=True)

    class Meta:
        db_table = 'messages'

    def __str__(self) -> str:
        """Строковое представление."""
        return 'Message {0}'.format(self.message_id)


@final
class User(AbstractUser):
    """Пользователь."""

    REQUIRED_FIELDS: ClassVar = ['chat_id']

    chat_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=128, unique=True)
    is_active = models.BooleanField(default=True)
    comment = models.CharField(max_length=128)
    day = models.IntegerField(default=2)
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True)
    referrer_id = models.ForeignKey('self', on_delete=models.PROTECT, null=True)
    legacy_id = models.BigIntegerField(null=True)

    class Meta:
        db_table = 'users'

    def __str__(self) -> str:
        """Строковое представление."""
        return 'User "{0}"'.format(self.chat_id)


@final
class UserAction(models.Model):
    """Действие пользователя."""

    user_action_id = models.BigAutoField(primary_key=True, editable=False)
    date_time = models.DateTimeField()
    action = models.CharField(max_length=16)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        db_table = 'user_actions'

    def __str__(self) -> str:
        """Строковое представление."""
        return 'UserAction {0}, {1}'.format(self.user_id, self.action)
