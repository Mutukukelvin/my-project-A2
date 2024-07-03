from django.urls import path
from . import views

urlpatterns = [
    path('create-bank/', views.create_bank, name='create_bank'),
    path('create-branch/', views.create_branch, name='create_branch'),
]
