from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.db import models

from task_manager.labels.models import Labels
from task_manager.labels.forms import LabelForm
from task_manager.mixins import NoPermissionMixin
from task_manager.text import LabelFlashMessages, TitleNames


label_messages = LabelFlashMessages()
title_names = TitleNames()


class LabelsIndexView(NoPermissionMixin, ListView):
    model = Labels
    template_name = 'labels/index.html'
    extra_context = {'title': title_names.labels}


class LabelCreateView(NoPermissionMixin, SuccessMessageMixin, CreateView):
    model = Labels
    form_class = LabelForm
    template_name = 'create.html'
    success_url = reverse_lazy('labels_index')
    success_message = label_messages.create_label
    extra_context = {'title': title_names.label_create}


class LabelUpdateView(NoPermissionMixin, SuccessMessageMixin, UpdateView):
    model = Labels
    form_class = LabelForm
    template_name = 'update.html'
    success_url = reverse_lazy('labels_index')
    success_message = label_messages.update_label
    extra_context = {'title': title_names.label_update}


class LabelDeleteView(NoPermissionMixin, SuccessMessageMixin, DeleteView):
    model = Labels
    template_name = 'delete.html'
    success_url = reverse_lazy('labels_index')
    success_message = label_messages.delete_label
    extra_context = {'title': title_names.label_delete}

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(self.request, label_messages.delete_label)
            return redirect(reverse_lazy('labels_index'))
        except models.ProtectedError:
            messages.error(self.request, label_messages.delete_protected_label)
            return redirect(reverse_lazy('labels_index'))
