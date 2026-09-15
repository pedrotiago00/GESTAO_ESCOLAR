from django.shortcuts import render, redirect
from .forms import LoginForms, CadastroForms
from .models import PerfilUsuario
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login


def login(request):
    form = LoginForms(request.POST or None)

    if request.method == 'POST':
        nome = (request.POST.get('username') or '').strip()
        senha = request.POST.get('password', '')

        erros = []

        if not nome or not senha:
            erros.append('Preencha todos os campos.')
        else:
            usuario = authenticate(request, username=nome, password=senha)
            if usuario is None:
                erros.append('Usuário ou senha inválidos.')

        if erros:
            return render(request, 'usuarios/login.html', {'form': form, 'erros': erros})

        auth_login(request, usuario)
        return redirect('dashboard')

    return render(request, 'usuarios/login.html', {'form': form})


def cadastro(request):
    form = CadastroForms(request.POST or None)

    if request.method == 'POST':
        nome = (request.POST.get('username') or '').strip()
        email = (request.POST.get('email') or '').strip()
        senha = request.POST.get('password', '')
        confirmar_senha = request.POST.get('password_confirm', '')
        escola_id = request.POST.get('escola')
        termos = request.POST.get('termos')

        erros = []

        if not nome or not email or not senha or not confirmar_senha or not escola_id:
            erros.append('Preencha todos os campos obrigatórios.')
        elif senha != confirmar_senha:
            erros.append('As senhas não conferem.')
        elif User.objects.filter(username=nome).exists():
            erros.append('Este nome de usuário já está em uso.')
        elif User.objects.filter(email=email).exists():
            erros.append('Este e-mail já está cadastrado.')
        elif not termos:
            erros.append('Você precisa aceitar os termos.')

        if erros:
            return render(request, 'usuarios/cadastro.html', {'form': form, 'erros': erros})

        usuario = User.objects.create_user(
            username=nome,
            email=email,
            password=senha,
        )

        PerfilUsuario.objects.create(
            usuario=usuario,
            escola_id=escola_id,
        )

        return redirect('login')

    return render(request, 'usuarios/cadastro.html', {'form': form})