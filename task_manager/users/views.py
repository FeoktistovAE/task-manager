from django.shortcuts import render, redirect
from django.views import View
from task_manager.users.models import Users
from task_manager.users.forms import UsersForm, UsersLoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
class UsersView(View):
    def get(self, request):
        users = Users.objects.all()
        return render(request, 'users/show.html', {'users': users})


class UsersFormCreateView(View):
    def get(self, request, *args, **kwargs):
        form = UsersForm
        return render(request, 'users/create.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = UsersForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'User succesfully created')
            return redirect('index')
        messages.add_message(request, messages.ERROR, "Something went wrong")
        return render(request, 'users/create.html', {'form': form})


class UsersFormEditView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = Users.objects.get(id=user_id)
        form = UsersForm(instance=user)
        return render(request, 'users/update.html', {'form': form, 'user_id': user_id})

    
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = Users.objects.get(id=user_id)
        form = UsersForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'User succesfully updated')
            return redirect('index')
        messages.add_message(request, messages.ERROR, 'Somethong went wrong')
        return render(request, 'users/update.html', {'form': form, 'user_id': user_id})


class UsersFormDeleteView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = Users.objects.get(id=user_id)
        full_name = user.get_full_name
        return render(request, 'users/delete.html', {'user_id': user_id, 'full_name': full_name})
    
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = Users.objects.get(id=user_id)
        if user:
            user.delete()
            messages.add_message(request, messages.SUCCESS, 'User succesfully deleted')
            return redirect('index')
        messages.add_message(request, messages.ERROR, 'Something went wrong')
        return redirect('index')


# class UsersFormLoginView(View):
#     def get(self, request, *args, **kwargs):
#         form = UsersLoginForm
#         return render(request, 'users/login.html', {'form': form})
    
#     def post(self, request, *args, ** kwargs):
#         username = request.POST['username']
#         password = request.POST['password']
#         form = UsersLoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             print(user)
#             if user is not None:
#                 login(request, user)
#                 messages.add_message(request, messages.SUCCESS, 'You are logged in')
#                 return redirect('index')
        
#         messages.add_message(request, messages.ERROR, 'Somethong went wrong')
#         return render(request, 'users/login.html', {'form': form})


class UsersFormLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UsersLoginForm
