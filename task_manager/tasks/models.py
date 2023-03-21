from django.db import models

from task_manager.users.models import Users
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels
from task_manager.text import FieldNames


field_names = FieldNames()


class Tasks(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        verbose_name=field_names.name
    )
    description = models.TextField(
        verbose_name=field_names.desctiption,
        blank=True
    )
    author = models.ForeignKey(
        Users,
        related_name='author',
        on_delete=models.PROTECT,
        verbose_name=field_names.author,
    )
    status = models.ForeignKey(
        Statuses,
        on_delete=models.PROTECT,
        verbose_name=field_names.status
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=field_names.date_created
    )
    executor = models.ForeignKey(
        Users,
        related_name='executor',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=field_names.executor
    )
    labels = models.ManyToManyField(
        Labels,
        related_name='label',
        blank=True,
        through='TasksToLabels',
        verbose_name=field_names.labels
    )

    def __str__(self):
        return self.name


class TasksToLabels(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    label = models.ForeignKey(Labels, on_delete=models.PROTECT)

    def __str__(self):
        return "{}_{}".format(self.task.__str__(), self.label.__str__())
