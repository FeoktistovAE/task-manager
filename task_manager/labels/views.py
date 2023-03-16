from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Labels
from task_manager.labels.forms import LabelForm
from task_manager.mixins import NoPermissionMixin


class LabelsIndexView(NoPermissionMixin, ListView):
    model = Labels
    template_name = 'labels/index.html'
    extra_context = {'title': _('Labels')}


class LabelCreateView(NoPermissionMixin, SuccessMessageMixin, CreateView):
    model = Labels
    form_class = LabelForm
    template_name = 'create.html'
    success_url = reverse_lazy('labels_index')
    success_message = _('Label succesfully created')
    extra_context = {'title': _('Create a label')}


class LabelUpdateView(NoPermissionMixin, SuccessMessageMixin, UpdateView):
    model = Labels
    form_class = LabelForm
    template_name = 'update.html'
    success_url = reverse_lazy('labels_index')
    success_message = _('Label successfully updated')
    extra_context = {'title': _('Update the label')}


class LabelDeleteView(NoPermissionMixin, SuccessMessageMixin, DeleteView):
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
