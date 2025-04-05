from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    is_agree_to_processing_personal_data = models.BooleanField(
        _('Согласен на обработку перс. данных'),
        default=False,
    )
    is_confirm_phone = models.BooleanField(
        _('Подтвердил номер телефона'),
        default=False,
    )
    is_confirm_email = models.BooleanField(
        _('Подтвердил адрес эл. почты'),
        default=False,
    )
    phone = models.CharField(_('Номер телефона'), max_length=16, blank=True)
    photo = models.ImageField(upload_to='accounts')

    class Meta:
        db_table = 'auth_user'
