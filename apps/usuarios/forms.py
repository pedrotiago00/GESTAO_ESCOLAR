from django import forms

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