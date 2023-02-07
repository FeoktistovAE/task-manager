from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from task_manager.users.models import Users


class UsersForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'username']


class UsersLoginForm(AuthenticationForm):
    class Meta:
        model = Users
        fields = ['username', 'password']
