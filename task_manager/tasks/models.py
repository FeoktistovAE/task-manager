from django.db import models

from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager import translation


class Task(models.Model):
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
        User,
        related_name='author',
        on_delete=models.PROTECT,
        verbose_name=translation.AUTHOR_FIELD,
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=translation.STATUS_FIELD
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=translation.DATE_CREATED_FIELD
    )
    executor = models.ForeignKey(
        User,
        related_name='executor',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=translation.EXECUTOR_FIELD
    )
    labels = models.ManyToManyField(
        Label,
        related_name='label',
        blank=True,
        through='TaskToLabel',
        verbose_name=translation.LABELS_FIELD
    )

    def __str__(self):
        return self.name


class TaskToLabel(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)

    def __str__(self):
        return "{}_{}".format(self.task.__str__(), self.label.__str__())
