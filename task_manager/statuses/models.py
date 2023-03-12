from django.db import models
from django.utils.translation import gettext_lazy as _


class Statuses(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        verbose_name=_('Name')
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
