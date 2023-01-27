from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from task_manager.users.models import Users


class UsersForm(ModelForm):
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'username', 'password']


class UsersLoginForm(AuthenticationForm):
    class Meta:
        model = Users
        fields = ['username', 'password']