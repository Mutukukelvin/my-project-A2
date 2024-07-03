from django.shortcuts import render,redirect

from .models import Bank

from .models import Branch

from .forms import Bank

from .forms import Branch

from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def create_bank(request):
    if request.method == 'POST':
        form = BankForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')  # redirect to'success URL' 
    else:
        form = BankForm()

    return render(request, 'bank-form.html', {'form': form})

@login_required
def create_branch(request):
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('') # redirect to'success URL' (profile view)
    else:
        form = BranchForm()

    return render(request, 'branch-form.html', {'form': form})

def home(request):
    return render(request, 'home.html')