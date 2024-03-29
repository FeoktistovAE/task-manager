from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.db import models

from task_manager.labels.models import Label
from task_manager.labels.forms import LabelForm
from task_manager.mixins import NoPermissionMixin
from task_manager import translation


class LabelsIndexView(NoPermissionMixin, ListView):
    model = Label
    template_name = 'labels/index.html'
    extra_context = {'title': translation.LABELS_TITLE}


class LabelCreateView(NoPermissionMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'create.html'
    success_url = reverse_lazy('labels_index')
    success_message = translation.LABEL_CREATE
    extra_context = {'title': translation.LABEL_CREATE_TITLE}


class LabelUpdateView(NoPermissionMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'update.html'
    success_url = reverse_lazy('labels_index')
    success_message = translation.LABEL_UPDATE
    extra_context = {'title': translation.LABEL_UPDATE_TITLE}


class LabelDeleteView(NoPermissionMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'delete.html'
    success_url = reverse_lazy('labels_index')
    success_message = translation.LABEL_DELETE
    extra_context = {'title': translation.LABEL_DELETE_TITLE}

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(self.request, translation.LABEL_DELETE)
            return redirect(reverse_lazy('labels_index'))
        except models.ProtectedError:
            messages.error(self.request, translation.DELETE_PROTECTED_LABEL)
            return redirect(reverse_lazy('labels_index'))
