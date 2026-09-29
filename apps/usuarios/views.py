from django.shortcuts import render, redirect
from .forms import LoginForms, CadastroForms
from .models import Funcao, PerfilUsuario
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.db import transaction
from apps.cadastros.models import Professores


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

    if request.method == 'POST' and form.is_valid():
        nome = form.cleaned_data['username']
        email = form.cleaned_data['email']

        if User.objects.filter(username=nome).exists():
            form.add_error('username', 'Este nome de usuário já está em uso.')
        elif User.objects.filter(email=email).exists():
            form.add_error('email', 'Este e-mail já está cadastrado.')
        else:
            with transaction.atomic():
                usuario = User.objects.create_user(
                    username=nome,
                    email=email,
                    password=form.cleaned_data['password'],
                )

                escola = form.cleaned_data['escola']
                funcao = form.cleaned_data['funcao']
                PerfilUsuario.objects.create(
                    usuario=usuario,
                    escola=escola,
                    funcao=funcao,
                )

                if funcao.nome.strip().casefold() == 'professor':
                    Professores.objects.create(
                        escola=escola,
                        matricula=form.cleaned_data['matricula'],
                        nome=form.cleaned_data['nome_completo'],
                        formacao=form.cleaned_data['formacao'],
                        disciplina=form.cleaned_data['disciplina'],
                        carga_horaria=form.cleaned_data['carga_horaria'],
                    )

            return redirect('login')

    return render(request, 'usuarios/cadastro.html', {'form': form})