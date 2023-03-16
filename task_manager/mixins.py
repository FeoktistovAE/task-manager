from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class NoPermissionMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please sign in.'))
        return redirect(reverse_lazy('user_login'))


class UserPassesUsernameTest(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return self.request.user.username == obj.username
