from task_manager.statuses.models import Statuses
from task_manager.statuses.forms import StatusForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.db import models


class StatusesIndexView(LoginRequiredMixin, ListView):
    model = Statuses
    template_name = 'statuses/index.html'

    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorized! Please sign in.')
        return redirect(reverse_lazy('user_login'))


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Statuses
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses_index')
    success_message = 'Status succesfully created'

    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorized! Please sign in.')
        return redirect(reverse_lazy('user_login'))


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin,  UpdateView):
    model = Statuses
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses_index')
    success_message = 'Status successfully updated'

    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorized! Please sign in.')
        return redirect(reverse_lazy('user_login'))


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Statuses
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses_index')

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(self.request, 'Status successfully deleted')
            return redirect(reverse_lazy('statuses_index'))
        except models.ProtectedError:
            messages.error(self.request, "Unable to delete status. It's in use")
            return redirect(reverse_lazy('statuses_index'))

    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorized! Please sign in.')
        return redirect(reverse_lazy('user_login'))
