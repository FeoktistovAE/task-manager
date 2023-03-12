from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django_filters.views import FilterView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import Tasks
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.filter import TaskFilter


class TasksIndexView(LoginRequiredMixin, FilterView):
    model = Tasks
    template_name = 'tasks/index.html'
    filterset_class = TaskFilter
    extra_context = {'title': _('Tasks')}

    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please sign in.'))
        return redirect(reverse_lazy('user_login'))


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Tasks
    template_name = 'tasks/detail.html'
    extra_context = {'title': _('Task view')}

    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please sign in.'))
        return redirect(reverse_lazy('user_login'))


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = TaskForm
    template_name = 'create.html'
    success_url = reverse_lazy('tasks_index')
    success_message = _('Task succesfully created')
    extra_context = {'title': _('Create a task')}

    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please sign in.'))
        return redirect(reverse_lazy('user_login'))

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tasks
    form_class = TaskForm
    template_name = 'update.html'
    success_url = reverse_lazy('tasks_index')
    success_message = _('Task successfully updated')
    extra_context = {'title': _('Update the task')}

    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please sign in.'))
        return redirect(reverse_lazy('user_login'))


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Tasks
    template_name = 'delete.html'
    success_url = reverse_lazy('tasks_index')
    success_message = _('Task successfully deleted')
    extra_context = {'title': _('Delete the task')}

    def test_func(self):
        obj = self.get_object()
        return self.request.user.id == obj.author.id

    def handle_no_permission(self):
        messages.error(self.request, _('A task can only be deleted by its author'))
        return redirect(reverse_lazy('tasks_index'))
