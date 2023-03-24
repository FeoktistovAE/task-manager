from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django_filters.views import FilterView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.filter import TaskFilter
from task_manager.mixins import NoPermissionMixin
from task_manager import translation


class TasksIndexView(NoPermissionMixin, FilterView):
    model = Task
    template_name = 'tasks/index.html'
    filterset_class = TaskFilter
    extra_context = {'title': translation.TASKS_TITLE}


class TaskDetailView(NoPermissionMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    extra_context = {'title': translation.TASK_DETAIL_TITLE}


class TaskCreateView(NoPermissionMixin, SuccessMessageMixin, CreateView):
    form_class = TaskForm
    template_name = 'create.html'
    success_url = reverse_lazy('tasks_index')
    success_message = translation.TASK_CREATE
    extra_context = {'title': translation.TASK_CREATE_TITLE}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(NoPermissionMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'update.html'
    success_url = reverse_lazy('tasks_index')
    success_message = translation.TASK_UPDATE
    extra_context = {'title': translation.TASK_UPDATE_TITLE}


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('tasks_index')
    success_message = translation.TASK_DELETE
    extra_context = {'title': translation.TASK_DELETE_TITLE}

    def test_func(self):
        obj = self.get_object()
        return self.request.user.id == obj.author.id

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, translation.NOT_AUTHORIZED_USER)
            return redirect(reverse_lazy('tasks_index'))
        messages.error(self.request, translation.NO_RIGHTS_TO_DELETE_TASK)
        return redirect(reverse_lazy('tasks_index'))
