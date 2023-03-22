from django.db import models
from task_manager import translation


class Statuses(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        verbose_name=translation.NAME_FIELD
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
