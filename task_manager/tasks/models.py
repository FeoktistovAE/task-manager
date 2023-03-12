from django.db import models
from task_manager.users.models import Users
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels
from django.utils.translation import gettext_lazy as _


class Tasks(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        verbose_name=_('Name')
    )
    description = models.TextField(
        verbose_name=_('Description'),
        blank=True
    )
    author = models.ForeignKey(
        Users,
        related_name='author',
        on_delete=models.PROTECT,
        verbose_name=_('Author'),
    )
    status = models.ForeignKey(
        Statuses,
        on_delete=models.PROTECT,
        verbose_name=_('Status')
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Date created')
    )
    executor = models.ForeignKey(
        Users,
        related_name='executor',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_('Executor')
    )
    labels = models.ManyToManyField(
        Labels,
        related_name='label',
        blank=True,
        through='TasksToLabels',
        verbose_name=_('Labels')
    )

    def __str__(self):
        return self.name


class TasksToLabels(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    label = models.ForeignKey(Labels, on_delete=models.PROTECT)

    def __str__(self):
        return "{}_{}".format(self.task.__str__(), self.label.__str__())
