from task_manager.statuses.models import Statuses
from task_manager.statuses.forms import StatusForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages


class StatusesView(LoginRequiredMixin, ListView):
    model = Statuses
    template_name = 'statuses/show.html'

    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorized! Please sign in.')
        return redirect(reverse_lazy('users_login'))


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Statuses
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses_show')
    success_message = 'Status succesfully created'

    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorized! Please sign in.')
        return redirect(reverse_lazy('users_login'))


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin,  UpdateView):
    model = Statuses
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses_show')
    success_message = 'Status successfully updated'

    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorized! Please sign in.')
        return redirect(reverse_lazy('users_login'))


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Statuses
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses_show')
    success_message = 'Status successfully deleted'

    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorized! Please sign in.')
        return redirect(reverse_lazy('users_login'))