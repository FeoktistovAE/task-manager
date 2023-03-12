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
from django.utils.translation import gettext_lazy as _


class StatusesIndexView(LoginRequiredMixin, ListView):
    model = Statuses
    template_name = 'statuses/index.html'
    extra_context = {'title': _('Statuses')}

    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please sign in.'))
        return redirect(reverse_lazy('user_login'))


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Statuses
    form_class = StatusForm
    template_name = 'create.html'
    success_url = reverse_lazy('statuses_index')
    success_message = _('Status succesfully created')
    extra_context = {'title': _('Create a status')}

    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please sign in.'))
        return redirect(reverse_lazy('user_login'))


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Statuses
    form_class = StatusForm
    template_name = 'update.html'
    success_url = reverse_lazy('statuses_index')
    success_message = _('Status successfully updated')
    extra_context = {'title': _('Update the status')}

    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please sign in.'))
        return redirect(reverse_lazy('user_login'))


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Statuses
    template_name = 'delete.html'
    success_url = reverse_lazy('statuses_index')
    extra_context = {'title': _('Delete the status')}

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(self.request, _('Status successfully deleted'))
            return redirect(reverse_lazy('statuses_index'))
        except models.ProtectedError:
            messages.error(self.request, _("Unable to delete status. It's in use"))
            return redirect(reverse_lazy('statuses_index'))

    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please sign in.'))
        return redirect(reverse_lazy('user_login'))
