from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from task_manager.text import UserFlashMessages

flash_message = UserFlashMessages()


class NoPermissionMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(self.request, flash_message.not_authorhorized_user)
        return redirect(reverse_lazy('user_login'))


class UserPassesUsernameTestMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return self.request.user.username == obj.username
