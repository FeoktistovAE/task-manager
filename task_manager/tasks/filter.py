import django_filters
from task_manager.tasks.models import Tasks
from task_manager.labels.models import Labels
from django import forms


class TaskFilter(django_filters.FilterSet):
    labels = django_filters.ModelChoiceFilter(
        queryset = Labels.objects.all(),
        label = 'Label'
    )
    client_tasks = django_filters.BooleanFilter(
        method='get_client_task',
        widget=forms.CheckboxInput,
        label='Only your own tasks'
    )
    def get_client_task(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(author=user)
        return queryset

    class Meta:
        model = Tasks
        fields = ['status', 'executor',]