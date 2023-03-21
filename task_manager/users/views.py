from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models

from task_manager.users.models import Users
from task_manager.users.forms import UsersForm, UsersLoginForm
from task_manager.mixins import UserPassesUsernameTestMixin
from task_manager.text import UserFlashMessages, TitleNames


flash_messages = UserFlashMessages()
title_names = TitleNames()


class UsersIndexView(ListView):
    model = Users
    template_name = 'users/index.html'
    extra_context = {'title': title_names.users}


class UserCreateView(SuccessMessageMixin, CreateView):
    model = Users
    form_class = UsersForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('user_login')
    success_message = flash_messages.create_user
    extra_context = {'title': title_names.user_create}


class UserUpdateView(SuccessMessageMixin, UserPassesUsernameTestMixin, LoginRequiredMixin, UpdateView):
    model = Users
    form_class = UsersForm
    template_name = 'update.html'
    success_url = reverse_lazy('users_index')
    success_message = flash_messages.update_user
    extra_context = {'title': title_names.user_update}

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, flash_messages.not_authorhorized_user)
            return redirect(reverse_lazy('user_login'))
        messages.error(self.request, flash_messages.no_rights_to_update_user)
        return redirect(reverse_lazy('users_index'))


class UserDeleteView(SuccessMessageMixin, UserPassesUsernameTestMixin, LoginRequiredMixin, DeleteView):
    model = Users
    success_url = reverse_lazy('users_index')
    success_message = flash_messages.delete_user
    template_name = 'delete.html'
    extra_context = {'title': title_names.user_delete}

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(self.request, flash_messages.delete_user)
            return redirect(reverse_lazy('users_index'))
        except models.ProtectedError:
            messages.error(self.request, flash_messages.delete_protected_user)
            return redirect(reverse_lazy('users_index'))

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, flash_messages.not_authorhorized_user)
            return redirect(reverse_lazy('user_login'))
        messages.error(self.request, flash_messages.no_rights_to_delete_user)
        return redirect(reverse_lazy('users_index'))


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UsersLoginForm
    success_message = flash_messages.login_user
    next_page = reverse_lazy('index')
    extra_context = {'title': title_names.user_login}


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, flash_messages.logout_user)
        return super().dispatch(request, *args, **kwargs)
