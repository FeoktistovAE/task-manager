from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.db import models

from task_manager.statuses.models import Statuses
from task_manager.statuses.forms import StatusForm
from task_manager.mixins import NoPermissionMixin
from task_manager.text import StatusFlashMessages, TitleNames


status_messages = StatusFlashMessages()
title_names = TitleNames()


class StatusesIndexView(NoPermissionMixin, ListView):
    model = Statuses
    template_name = 'statuses/index.html'
    extra_context = {'title': title_names.statuses}


class StatusCreateView(NoPermissionMixin, SuccessMessageMixin, CreateView):
    model = Statuses
    form_class = StatusForm
    template_name = 'create.html'
    success_url = reverse_lazy('statuses_index')
    success_message = status_messages.create_status
    extra_context = {'title': title_names.status_create}


class StatusUpdateView(NoPermissionMixin, SuccessMessageMixin, UpdateView):
    model = Statuses
    form_class = StatusForm
    template_name = 'update.html'
    success_url = reverse_lazy('statuses_index')
    success_message = status_messages.update_status
    extra_context = {'title': title_names.status_update}


class StatusDeleteView(NoPermissionMixin, SuccessMessageMixin, DeleteView):
    model = Statuses
    template_name = 'delete.html'
    success_url = reverse_lazy('statuses_index')
    extra_context = {'title': title_names.status_delete}

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(self.request, status_messages.delete_status)
            return redirect(reverse_lazy('statuses_index'))
        except models.ProtectedError:
            messages.error(self.request, status_messages.delete_protected_status)
            return redirect(reverse_lazy('statuses_index'))
