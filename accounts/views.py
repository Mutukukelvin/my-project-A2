from django.shortcuts import render, redirect

from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import login, logout

from django.http import JsonResponse, HttpResponse

from django.contrib.auth.decorators import login_required

from .forms import RegisterForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
                                                #i'll need to make changes to enable automatic login here
            return redirect('/accounts/login/')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/accounts/profile/view/')
        else:
            error_message = 'Username or password is invalid'
            return render(request, 'accounts/login.html', {'form': form, 'error_message': error_message})
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')


def home(request):
    return render(request, 'home.html')
