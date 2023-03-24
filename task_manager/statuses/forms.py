from task_manager.statuses.models import Status
from django.forms import ModelForm


class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = ['name']
