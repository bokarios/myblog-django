from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully.')
            return redirect('/users/login')

    else:
        form = RegisterForm()

    context = {
        'title': 'Register',
        'form': form
    }
    return render(request, 'users/register.html', context)

@login_required
def profile(request):
    context = {
        'title': 'Profile',
    }
    return render(request, 'users/profile.html', context)
