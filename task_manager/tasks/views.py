from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

from task_manager.tasks.models import Tasks
from task_manager.tasks.forms import TaskForm


class TasksIndexView(LoginRequiredMixin, ListView):
    model = Tasks
    template_name = 'tasks/index.html'

    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorized! Please sign in.')
        return redirect(reverse_lazy('user_login'))


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Tasks
    template_name = 'tasks/detail.html'

    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorized! Please sign in.')
        return redirect(reverse_lazy('user_login'))


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks_index')
    success_message = 'Task succesfully created'

    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorized! Please sign in.')
        return redirect(reverse_lazy('user_login'))

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tasks
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks_index')
    success_message = 'Task successfully updated'

    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorized! Please sign in.')
        return redirect(reverse_lazy('user_login'))


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Tasks
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks_index')
    success_message = 'Task successfully deleted'

    def test_func(self):
        obj = self.get_object()
        return self.request.user.id == obj.author.id

    def handle_no_permission(self):
        messages.error(self.request, 'A task can only be deleted by its author')
        return redirect(reverse_lazy('tasks_index'))
