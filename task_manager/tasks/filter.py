import django_filters
from django import forms

from task_manager.tasks.models import Tasks
from task_manager.labels.models import Labels
from task_manager import translation


class TaskFilter(django_filters.FilterSet):
    labels = django_filters.ModelChoiceFilter(
        queryset=Labels.objects.all(),
        label=translation.LABEL_FIELD,
    )
    client_tasks = django_filters.BooleanFilter(
        method='get_client_task',
        widget=forms.CheckboxInput,
        label=translation.OWN_TASKS_FIELD,
    )

    def get_client_task(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(author=user)
        return queryset

    class Meta:
        model = Tasks
        fields = ['status', 'executor']
