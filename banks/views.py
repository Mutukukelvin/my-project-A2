from django.shortcuts import render,redirect, get_object_or_404

from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, HttpResponseForbidden

from .models import Bank

from .models import Branch

from .forms import BankForm,BranchForm

from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from django.urls import reverse

# Create your views here.
@login_required
def add_bank(request):
    if not request.user.is_authenticated:
        return redirect(f'/accounts/login/?next=/banks/add/')
    if request.method == 'POST':
        form = BankForm(request.POST)
        if form.is_valid():
            bank = form.save(commit=False)
            bank.owner = request.user  
            bank.save()
            return redirect(reverse('banks:bank_details', args=[bank.id]))
             #Success URL: /banks/<bank_id>/details/

    else:
        form = BankForm()

    return render(request, 'banks/add.html', {'form': form})

@login_required
def add_branch(request, bank_id):
    bank = get_object_or_404(Bank, id=bank_id)

    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            branch = form.save(commit=False)
            branch.bank = bank  
            branch.save()
            return redirect('banks:branch_details', branch_id=branch.id)
    else:
        form = BranchForm()

    return render(request, 'banks/branches/add.html', {'form': form, 'bank': bank})


def banks_accounts_view(request):
   banks = Bank.objects.all()
   branch = Branch.objects.all()
   return render(request, 'banks/banks_accounts.html', {'banks': banks, 'branch': branch})

def home(request):
     return render(request, 'banks/home.html')

def list_banks(request):
    banks = Bank.objects.all()
    return render(request, 'banks/list_banks.html', {'banks': banks})

def bank_details(request, bank_id):
    bank = get_object_or_404(Bank, id=bank_id)
    branches = Branch.objects.filter(bank=bank)
    return render(request, 'banks/details.html', {'bank': bank, 'branches': branches})

@login_required
def branch_details(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    data = {
        'id': branch.id,
        'name': branch.name,
        'transit_number': branch.transit_number,
        'address': branch.address,
        'email': branch.email,
        'capacity': branch.capacity,
        'last_modified': branch.last_modified.isoformat()
    }
    return JsonResponse(data)

@login_required
def edit_branch(request, bank_id):
    branch = get_object_or_404(Branch, bank_id=bank_id) 
    if request.method == 'POST':
        form = BranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            return redirect('/branch/detail.html', bank_id=branch.bank_id)  
    else:
        form = BranchForm(instance=branch)
    
    return render(request, 'banks/branch/edit.html', {'form': form})