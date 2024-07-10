from django import forms

from .models import Bank

from .models import Branch

class BankForm(forms.ModelForm):
    class Meta:
        model=Bank
        fields=['name', 'description','institution_number','swift_code',]


class BranchForm(forms.ModelForm):
    class Meta:
        model=Branch
        fields=['name', 'transit_number', 'address', 'email', 'capacity',]
