from django.db import models
from task_manager.users.models import Users
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels


class Tasks(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    author = models.ForeignKey(Users, related_name='author', on_delete=models.PROTECT)
    status = models.ForeignKey(Statuses, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)
    executor = models.ForeignKey(Users, related_name='executor', null=True, on_delete=models.PROTECT)
    labels = models.ManyToManyField(Labels, related_name='label', blank=True, through='TasksToLabels')

    def __str__(self):
        return self.name


class TasksToLabels(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    label = models.ForeignKey(Labels, on_delete=models.PROTECT)

    def __str__(self):
        return "{}_{}".format(self.task.__str__(), self.label.__str__())
