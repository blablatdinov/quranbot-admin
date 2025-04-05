from django.db import models
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    name = models.CharField(_('Post name'), max_length=128)

    def __str__(self):
        return f'Post. name={self.name}'
