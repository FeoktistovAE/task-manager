from django.db import models

# Create your models here.
class Statuses(models.Model):
    name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

