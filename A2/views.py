from django.shortcuts import render
from banks.models import Bank, Branch

def banks_accounts_view(request):
   banks = Bank.objects.all()
   branch = Branch.objects.all()
   return render(request, 'banks/banks_accounts.html', {'banks': banks, 'branch': branch})
