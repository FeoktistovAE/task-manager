from django.db import models
from task_manager.text import FieldNames


field_names = FieldNames()


class Statuses(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        verbose_name=field_names.name
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
