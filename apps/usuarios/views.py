from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from .forms import LoginForms, CadastroForms

def login(request):
    form = LoginForms()
    return render(request, 'usuarios/login.html', {'form': form})

def cadastro(request):
    form = CadastroForms()
    if request.method == 'POST':
        form = CadastroForms(request.POST)
        if form['password'].data != form['password_confirm'].data:
            return redirect('cadastro')

    return render(request, 'usuarios/cadastro.html', {'form': form})