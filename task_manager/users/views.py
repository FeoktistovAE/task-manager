from task_manager.users.models import Users
from task_manager.users.forms import UsersForm, UsersLoginForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class UsersIndexView(ListView):
    model = Users
    template_name = 'users/index.html'
    extra_context = {'title': _('Users')}


class UserCreateView(SuccessMessageMixin, CreateView):
    model = Users
    form_class = UsersForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('user_login')
    success_message = _('User has created')
    extra_context = {'title': _('Create a user')}


class UserUpdateView(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Users
    form_class = UsersForm
    template_name = 'update.html'
    success_url = reverse_lazy('users_index')
    success_message = _('User succesfully updated')
    extra_context = {'title': _('Update the user')}

    def test_func(self):
        obj = self.get_object()
        return self.request.user.username == obj.username

    def handle_no_permission(self):
        return redirect(reverse_lazy('users_index'))


class UserDeleteView(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Users
    success_url = reverse_lazy('users_index')
    success_message = _('User successfully deleted')
    template_name = 'delete.html'
    extra_context = {'title': _('Delete the user')}

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(self.request, _('User successfully deleted'))
            return redirect(reverse_lazy('users_index'))
        except models.ProtectedError:
            messages.error(self.request, _("Unable to delete user. He's in use"))
            return redirect(reverse_lazy('users_index'))

    def test_func(self):
        obj = self.get_object()
        return self.request.user.username == obj.username

    def handle_no_permission(self):
        return redirect(reverse_lazy('users_index'))


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UsersLoginForm
    success_message = _('You are logged in')
    next_page = reverse_lazy('users_index')
    extra_context = {'title': _('Вход')}


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, _('You are logged out'))
    return redirect('index')
