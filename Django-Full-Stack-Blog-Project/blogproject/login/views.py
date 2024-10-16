from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .form import RegisterForm, LoginForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from .models import User
from django.contrib.auth import authenticate, login, logout



# Create your views here.

# class RegisterView(CreateView):
#     model = User
#     #fields = '__all__' 
#     form_class = UserForm
#     template_name = "login/register.html"
#     success_url = "/login/register"


def RegisterView(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
    context = {
        'form':form
    }
    return render(request, "login/register.html", context)


def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Pass the user object here, not the username
            return HttpResponseRedirect("/")  # Use the correct URL
        else:
            context = {
                'form': LoginForm(),
                'error': 'Invalid username or password'
            }
            return render(request, "login/login.html", context)
    
    context = {
        'form': LoginForm()
    }
    return render(request, "login/login.html", context)


def logoutUser(request):
    logout(request)
    return HttpResponseRedirect("login")