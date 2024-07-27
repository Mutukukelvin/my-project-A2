from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'banks'

urlpatterns = [
    
    path('', views.home, name='home'),

    path('banks_accounts/', views.banks_accounts_view, name='banks_accounts'),

    path('add/', views.add_bank, name='add_bank'),

    path('details/<int:bank_id>/', views.bank_details, name='bank_details'),

    path('<int:bank_id>/branches/add/', views.add_branch, name='add_branch'),

    path('all/', views.list_banks, name='list_banks'),

    path('branch/<int:branch_id>/details/', views.branch_details, name='branch_details'),

    path('details/<int:bank_id>/edit/', views.edit_branch, name='edit_branch'),


]
