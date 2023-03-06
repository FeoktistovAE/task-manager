from django.urls import path
from task_manager.users import views

urlpatterns = [
    path('', views.UsersIndexView.as_view(), name='users_index'),
    path('create/', views.UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_destroy'),
]
