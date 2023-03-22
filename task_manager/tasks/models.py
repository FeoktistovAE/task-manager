from django.db import models

from task_manager.users.models import Users
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels
from task_manager import translation


class Tasks(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        verbose_name=translation.NAME_FIELD
    )
    description = models.TextField(
        verbose_name=translation.DESCRIPTION_FIELD,
        blank=True
    )
    author = models.ForeignKey(
        Users,
        related_name='author',
        on_delete=models.PROTECT,
        verbose_name=translation.AUTHOR_FIELD,
    )
    status = models.ForeignKey(
        Statuses,
        on_delete=models.PROTECT,
        verbose_name=translation.STATUS_FIELD
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=translation.DATE_CREATED_FIELD
    )
    executor = models.ForeignKey(
        Users,
        related_name='executor',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=translation.EXECUTOR_FIELD
    )
    labels = models.ManyToManyField(
        Labels,
        related_name='label',
        blank=True,
        through='TasksToLabels',
        verbose_name=translation.LABELS_FIELD
    )

    def __str__(self):
        return self.name


class TasksToLabels(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    label = models.ForeignKey(Labels, on_delete=models.PROTECT)

    def __str__(self):
        return "{}_{}".format(self.task.__str__(), self.label.__str__())
