from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django import forms 
from .forms import MyAuthenticationForm
# Create your views here.
class MyLoginView(LoginView):
    form_class = MyAuthenticationForm
