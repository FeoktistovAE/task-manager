from django.db import models
from task_manager.users.models import Users
from task_manager.statuses.models import Statuses


class Tasks(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(Users, related_name='author', on_delete=models.PROTECT)
    status = models.ForeignKey(Statuses, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)
    executor = models.ForeignKey(Users, related_name='executor', null=True, on_delete=models.PROTECT)
