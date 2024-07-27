from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.urls import reverse
from django.views.generic import FormView
from accounts.forms.profile import ProfileEditForm
from accounts.forms.register import RegisterForm
from django.contrib.auth.models import User
from django.template.response import TemplateResponse


from django.contrib import messages

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user:
                login(request, user)
                return redirect('/accounts/profile/view/')
            return redirect('/accounts/login/')  # Success URL: /accounts/login/
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        next_url = request.POST.get('next', '/accounts/profile/view/')
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(next_url)
        else:
            error_message = 'Username or password is invalid'
            return render(request, 'accounts/login.html', {'form': form, 'error_message': error_message})
    else:
        next_url = request.GET.get('next', '/accounts/profile/view/')
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})

def logout_view(request):
    logout(request)
    next_url = request.GET.get('next', '/banks/')  # for logging out in banks app
    return redirect(next_url)

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
            try:
                validate_email(email)
                user.email = email
            except ValidationError:
                return render(request, 'accounts/profile/edit_profile.html', {
                    'error_message': "Enter a valid email address",
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                })

        if password1:
            if password1 == password2:
                if len(password1) < 8:
                    return render(request, 'accounts/profile/edit_profile.html', {
                        'error_message': "This password is too short. It must contain at least 8 characters",
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name
                    })
                user.set_password(password1)
            else:
                return render(request, 'accounts/profile/edit_profile.html', {
                    'error_message': "The two password fields didn't match",
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                })

        user.save()
        login(request, user)  # For keeping me loged in after changing password
        return redirect('/accounts/profile/view/')

    return render(request, 'accounts/profile/edit_profile.html', {
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name
    })

class Register(FormView):
    template_name = "accounts/register.html"
    form_class = RegisterForm

    def get_success_url(self):
        return reverse("accounts:login")

    def form_valid(self, form):
        form.cleaned_data.pop("password2")
        User.objects.create_user(**form.cleaned_data)
        return super().form_valid(form)

def profile_view(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            user = User.objects.get(id=request.user.id)
            return JsonResponse({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            })
    else:
        return HttpResponse("Unauthorized", status=401)

def edit_profile(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            user = User.objects.get(id=request.user.id)

            form = ProfileEditForm(
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
            )
            return TemplateResponse(
                request, "accounts/edit_profile.html", context={"form": form}
            )
        else:
            form = ProfileEditForm(request.POST)
            if form.is_valid():
                user = User.objects.get(id=request.user.id)
                if form.cleaned_data.get("password"):
                    user.password = form.cleaned_data["password"]
                user.first_name = form.cleaned_data["first_name"]
                user.last_name = form.cleaned_data["last_name"]
                user.email = form.cleaned_data["email"]
                user.save()
                login(request, user)
                return HttpResponseRedirect(reverse("accounts:profile"), status=302)
            else:
                return TemplateResponse(
                    request, "accounts/edit_profile.html", context={"form": form}, status=302
                )
    else:
        return HttpResponse("Unauthorized", status=401)
    

   
