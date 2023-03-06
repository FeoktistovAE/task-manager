from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.get_full_name
