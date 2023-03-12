from task_manager.labels.models import Labels
from task_manager.labels.forms import LabelForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.db import models
from django.utils.translation import gettext_lazy as _


class LabelsIndexView(LoginRequiredMixin, ListView):
    model = Labels
    template_name = 'labels/index.html'
    extra_context = {'title': _('Labels')}

    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please sign in.'))
        return redirect(reverse_lazy('user_login'))


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Labels
    form_class = LabelForm
    template_name = 'create.html'
    success_url = reverse_lazy('labels_index')
    success_message = _('Label succesfully created')
    extra_context = {'title': _('Create a label')}

    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please sign in.'))
        return redirect(reverse_lazy('user_login'))


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Labels
    form_class = LabelForm
    template_name = 'update.html'
    success_url = reverse_lazy('labels_index')
    success_message = _('Label successfully updated')
    extra_context = {'title': _('Update the label')}

    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please sign in.'))
        return redirect(reverse_lazy('user_login'))


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Labels
    template_name = 'delete.html'
    success_url = reverse_lazy('labels_index')
    success_message = _('Label successfully deleted')
    extra_context = {'title': _('Delete the label')}

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(self.request, _('Label successfully deleted'))
            return redirect(reverse_lazy('labels_index'))
        except models.ProtectedError:
            messages.error(self.request, _("Unable to delete label. It's in use"))
            return redirect(reverse_lazy('labels_index'))

    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please sign in.'))
        return redirect(reverse_lazy('user_login'))
