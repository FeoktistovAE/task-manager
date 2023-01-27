from django.urls import path, include
from task_manager.users import views

urlpatterns = [
    path('', views.UsersView.as_view(), name='users_show'),
    path('create/', views.UsersFormCreateView.as_view(), name='users_create'),
    path('<int:pk>/edit/', views.UsersFormEditView.as_view(), name='users_edit'),
    path('<int:pk>/delete/', views.UsersFormDeleteView.as_view(), name='users_destroy'),
]