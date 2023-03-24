from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect

from task_manager import translation


class NoPermissionMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(self.request, translation.NOT_AUTHORIZED_USER)
        return redirect(reverse_lazy('user_login'))


class UserPassesUsernameTestMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return self.request.user.username == obj.username


class UsernameCheckMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, translation.NOT_AUTHORIZED_USER)
            return redirect(reverse_lazy('user_login'))
        messages.error(self.request, self.no_rights_message)
        return redirect(reverse_lazy('users_index'))
