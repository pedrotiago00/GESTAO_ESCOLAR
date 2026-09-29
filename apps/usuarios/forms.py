from django import forms

from apps.cadastros.models import Disciplinas, Professores

from .models import Escola, Funcao

class LoginForms(forms.Form):
    username = forms.CharField(
        label='Nome de usuário',
        max_length=150,
        required=True)

    password = forms.CharField(
        label='Senha',
        max_length=70,
        widget=forms.PasswordInput,
        required=True)

class CadastroForms(forms.Form):
    username = forms.CharField(
        label='Nome de usuário',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu nome de usuário'}))

    email = forms.EmailField(
        label='E-mail',
        max_length=100,
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'seu@email.com'}))

    escola = forms.ModelChoiceField(
        label='Escola',
        queryset=Escola.objects.filter(ativo=True).order_by('nome'),
        empty_label='Selecione a escola',
        required=True,
    )

    funcao = forms.ModelChoiceField(
        label='Função',
        queryset=Funcao.objects.order_by('nome'),
        empty_label='Selecione a função',
        required=True,
    )

    nome_completo = forms.CharField(
        label='Nome completo',
        max_length=100,
        required=False,
    )

    matricula = forms.CharField(
        label='Matrícula',
        max_length=20,
        required=False,
    )

    formacao = forms.CharField(
        label='Formação',
        max_length=100,
        required=False,
    )

    disciplina = forms.ModelChoiceField(
        label='Disciplina',
        queryset=Disciplinas.objects.filter(escola__ativo=True, status='Ativa').order_by('escola__nome', 'nome'),
        empty_label='Selecione a disciplina',
        required=False,
    )

    carga_horaria = forms.IntegerField(
        label='Carga horária semanal',
        min_value=1,
        required=False,
    )

    password = forms.CharField(
        label='Senha',
        max_length=70,
        widget=forms.PasswordInput,
        required=True)

    password_confirm = forms.CharField(
        label='Confirmar Senha',
        max_length=70,
        widget=forms.PasswordInput,
        required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        escola_id = self.data.get('escola')
        if escola_id and str(escola_id).isdecimal():
            self.fields['disciplina'].queryset = self.fields['disciplina'].queryset.filter(escola_id=escola_id)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'As senhas não conferem.')

        funcao = cleaned_data.get('funcao')
        if funcao and funcao.nome.strip().casefold() == 'professor':
            campos_docente = ('nome_completo', 'matricula', 'formacao', 'disciplina', 'carga_horaria')
            for campo in campos_docente:
                if not cleaned_data.get(campo):
                    self.add_error(campo, 'Este campo é obrigatório para cadastro de professor.')

            escola = cleaned_data.get('escola')
            disciplina = cleaned_data.get('disciplina')
            matricula = cleaned_data.get('matricula')
            if escola and disciplina and disciplina.escola_id != escola.pk:
                self.add_error('disciplina', 'Selecione uma disciplina da escola informada.')
            if escola and matricula and Professores.objects.filter(escola=escola, matricula=matricula).exists():
                self.add_error('matricula', 'Esta matrícula já está cadastrada na escola informada.')

        return cleaned_data