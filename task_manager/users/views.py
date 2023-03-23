from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db import models

from task_manager.users.models import Users
from task_manager.users.forms import UsersForm, UsersLoginForm
from task_manager.mixins import UserPassesUsernameTestMixin, UsernameCheckMixin
from task_manager import translation


class UsersIndexView(ListView):
    model = Users
    template_name = 'users/index.html'
    extra_context = {'title': translation.USERS_TITLE}


class UserCreateView(SuccessMessageMixin, CreateView):
    model = Users
    form_class = UsersForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('user_login')
    success_message = translation.USER_CREATE
    extra_context = {'title': translation.USER_CREATE_TITLE}


class UserUpdateView(
    SuccessMessageMixin,
    UserPassesUsernameTestMixin,
    UsernameCheckMixin,
    UpdateView
):
    def __init__(self):
        self.message = translation.NO_RIGHTS_TO_UPDATE_USER

    model = Users
    form_class = UsersForm
    template_name = 'update.html'
    success_url = reverse_lazy('users_index')
    success_message = translation.USER_UPDATE
    extra_context = {'title': translation.USER_CREATE_TITLE}


class UserDeleteView(
    SuccessMessageMixin,
    UserPassesUsernameTestMixin,
    UsernameCheckMixin,
    DeleteView
):
    def __init__(self):
        self.message = translation.NO_RIGHTS_TO_DELETE_USER

    model = Users
    success_url = reverse_lazy('users_index')
    success_message = translation.USER_DELETE
    template_name = 'delete.html'
    extra_context = {'title': translation.USER_DELETE_TITLE}

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(self.request, translation.USER_DELETE)
            return redirect(reverse_lazy('users_index'))
        except models.ProtectedError:
            messages.error(self.request, translation.DELETE_PROTECTED_USER)
            return redirect(reverse_lazy('users_index'))


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UsersLoginForm
    success_message = translation.USER_LOGIN
    next_page = reverse_lazy('index')
    extra_context = {'title': translation.USER_LOGIN_TITLE}


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, translation.USER_LOGOUT)
        return super().dispatch(request, *args, **kwargs)
