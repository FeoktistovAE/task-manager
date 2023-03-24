from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.db import models

from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusForm
from task_manager.mixins import NoPermissionMixin
from task_manager import translation


class StatusesIndexView(NoPermissionMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    extra_context = {'title': translation.STATUSES_TITLE}


class StatusCreateView(NoPermissionMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'create.html'
    success_url = reverse_lazy('statuses_index')
    success_message = translation.STATUS_CREATE
    extra_context = {'title': translation.STATUS_CREATE_TITLE}


class StatusUpdateView(NoPermissionMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'update.html'
    success_url = reverse_lazy('statuses_index')
    success_message = translation.STATUS_UPDATE
    extra_context = {'title': translation.STATUS_UPDATE_TITLE}


class StatusDeleteView(NoPermissionMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'delete.html'
    success_url = reverse_lazy('statuses_index')
    extra_context = {'title': translation.STATUS_DELETE_TITLE}

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(self.request, translation.STATUS_DELETE)
            return redirect(reverse_lazy('statuses_index'))
        except models.ProtectedError:
            messages.error(self.request, translation.DELETE_PROTECTED_STATUS)
            return redirect(reverse_lazy('statuses_index'))
