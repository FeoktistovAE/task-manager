from task_manager.statuses.models import Statuses
from django.forms import ModelForm


class StatusForm(ModelForm):
    class Meta:
        model = Statuses
        fields = ['name']