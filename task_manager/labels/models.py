from django.db import models


class Labels(models.Model):
    name = models.CharField(max_length=255, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(Labels, self).save(*args, **kwargs)
