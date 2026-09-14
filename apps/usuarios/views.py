from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, render
from .models import Usuarios

def login(request):
    return render(request, 'usuarios/login.html')

def cadastro(request):
    return render(request, 'usuarios/cadastro.html')