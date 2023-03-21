from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django_filters.views import FilterView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

from task_manager.tasks.models import Tasks
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.filter import TaskFilter
from task_manager.mixins import NoPermissionMixin
from task_manager.text import UserFlashMessages, TaskFlashMessages, TitleNames


user_messages = UserFlashMessages()
task_messages = TaskFlashMessages()
title_names = TitleNames()


class TasksIndexView(NoPermissionMixin, FilterView):
    model = Tasks
    template_name = 'tasks/index.html'
    filterset_class = TaskFilter
    extra_context = {'title': title_names.tasks}


class TaskDetailView(NoPermissionMixin, DetailView):
    model = Tasks
    template_name = 'tasks/detail.html'
    extra_context = {'title': title_names.task_detail}


class TaskCreateView(NoPermissionMixin, SuccessMessageMixin, CreateView):
    form_class = TaskForm
    template_name = 'create.html'
    success_url = reverse_lazy('tasks_index')
    success_message = task_messages.create_task
    extra_context = {'title': title_names.task_create}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(NoPermissionMixin, SuccessMessageMixin, UpdateView):
    model = Tasks
    form_class = TaskForm
    template_name = 'update.html'
    success_url = reverse_lazy('tasks_index')
    success_message = task_messages.update_task
    extra_context = {'title': title_names.task_update}


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Tasks
    template_name = 'delete.html'
    success_url = reverse_lazy('tasks_index')
    success_message = task_messages.delete_task
    extra_context = {'title': title_names.task_delete}

    def test_func(self):
        obj = self.get_object()
        return self.request.user.id == obj.author.id

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, user_messages.not_authorhorized_user)
            return redirect(reverse_lazy('tasks_index'))
        messages.error(self.request, task_messages.no_rights_to_delete_task)
        return redirect(reverse_lazy('tasks_index'))
