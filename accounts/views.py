from django.shortcuts import render, redirect

from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import login, logout

from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

from .forms import RegisterForm


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/accounts/login.html')#Success URL: /accounts/login/
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/accounts/profile/view/')#Success URL: /accounts/profile/view/
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
    return render(request, 'accounts/home.html')


@login_required
def view_profile(request):
    user = request.user
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name
    }
    return JsonResponse(user_data)


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email

        if password1:
            if password1 == password2:

                user.set_password(password1)

                user.save()
                
                return redirect('/accounts/profile/view/')#Success URL: /accounts/profile/view/
            else:
                error_message = "The two password fields didn't match"
                return render(request, 'accounts/edit_profile.html', {
                    'error_message': error_message,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                })

        user.save()
        return redirect('/accounts/profile/view/')

    return render(request, 'accounts/edit_profile.html', {
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name
    })