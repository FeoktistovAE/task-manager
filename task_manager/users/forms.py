from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from task_manager.users.models import User


class UsersForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class UsersLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
