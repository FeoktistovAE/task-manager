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


class UsersIndexView(ListView):
    model = Users
    template_name = 'users/index.html'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = Users
    form_class = UsersForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('user_login')
    success_message = 'User has created'


class UserUpdateView(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Users
    form_class = UsersForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users_index')
    success_message = 'User succesfully updated'

    def test_func(self):
        obj = self.get_object()
        return self.request.user.username == obj.username

    def handle_no_permission(self):
        return redirect(reverse_lazy('users_index'))


class UserDeleteView(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Users
    success_url = reverse_lazy('users_index')
    success_message = 'User successfully deleted'
    template_name = 'users/delete.html'

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(self.request, 'User successfully deleted')
            return redirect(reverse_lazy('users_index'))
        except models.ProtectedError:
            messages.error(self.request, "Unable to delete user. He's in use")
            return redirect(reverse_lazy('users_index'))

    def test_func(self):
        obj = self.get_object()
        return self.request.user.username == obj.username

    def handle_no_permission(self):
        return redirect(reverse_lazy('users_index'))


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UsersLoginForm
    success_message = 'You are logged in'
    next_page = reverse_lazy('users_index')


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'You are logged out')
    return redirect('index')
