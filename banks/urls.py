from django.urls import path
from . import views

app_name = 'banks' 

urlpatterns = [
    path('', views.home, name='home'),  

    path('banks_accounts/', views.banks_accounts_view, name='banks_accounts'),  

    path('banks/', views.add_bank, name='add_bank'),

    path('banks/', views.bank_details, name='bank_details'),

    path('banks', views.add_branch, name='add_branch'),

    path('all/', views.list_banks, name='list_banks'),

    path('branch/<int:branch_id>/details/', views.branch_details, name='branch_details'),
    
    path('branch/<int:branch_id>/edit/', views.edit_branch, name='edit_branch')
]
