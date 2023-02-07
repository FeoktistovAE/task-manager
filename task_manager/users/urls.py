from django.urls import path
from task_manager.users import views

urlpatterns = [
    path('', views.UsersView.as_view(), name='users_show'),
    path('create/', views.UsersCreateView.as_view(), name='users_create'),
    path('<int:pk>/edit/', views.UsersUpdateView.as_view(), name='users_edit'),
    path('<int:pk>/delete/', views.UsersDeleteView.as_view(), name='users_destroy'),
]
