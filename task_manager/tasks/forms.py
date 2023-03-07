from task_manager.tasks.models import Tasks
from django.forms import ModelForm


class TaskForm(ModelForm):
    class Meta:
        model = Tasks
        fields = ['name', 'description', 'status', 'executor', 'labels']
