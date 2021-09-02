from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.forms import CharField, PasswordInput, EmailField, EmailInput, TextInput, Select, Form
from django.forms.fields import ChoiceField
from apps.user_app.validators import *


class SignUpForm(UserCreationForm):

    username = CharField(
        label='Nome de Usuário',
        max_length=150,
        widget=TextInput(attrs={
            'class': 'form-control',
            'id': 'usernameInput',
            'placeholder': 'Nome de usuário'}))
    email = EmailField(
        label='E-mail',
        max_length=255,
        widget=EmailInput(attrs={
            'class': 'form-control',
            'id': 'emailInput',
            'placeholder': 'E-mail'}))
    first_name = CharField(
        label='Primeiro nome',
        max_length=100,
        widget=TextInput(attrs={
            'class': 'form-control',
            'id': 'fnameInput',
            'placeholder': 'Primeiro Nome'}))
    last_name = CharField(
        label='Último nome',
        max_length=100,
        widget=TextInput(attrs={
            'class': 'form-control',
            'id': 'lnameInput',
            'placeholder': 'Último Nome'}))
    password1 = CharField(
        label=("Senha"),
        strip=False,
        widget=PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control',
            'id': 'passwd1',
            'placeholder': 'Senha'}),)
    password2 = CharField(
        label=("Confirmação de senha"),
        strip=False,
        widget=PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control',
            'id': 'passwd1',
            'placeholder': 'Senha'}),)

    def clean(self):
        # Clean username
        username = self.cleaned_data['username']
        lista_erros = {'username': []}
        comprimento_minimo_username(username, lista_erros)
        verifica_username_existente(username, lista_erros)
        if lista_erros['username']:
            for erro in lista_erros['username']:
                self.add_error('username', erro)

        # Clean email
        email = self.cleaned_data.get('email')
        lista_erros = {'email': []}
        verifica_email_existente(email, lista_erros)
        for erro in lista_erros['email']:
            self.add_error('email', erro)
        return self.cleaned_data

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = 'email', 'username', 'first_name', 'last_name'


class LoginForm(AuthenticationForm):
    username = EmailField(label='E-mail', widget=EmailInput(attrs={'class': 'form-control',
        'placeholder': 'nome@dominio.com.br',
        'id': 'emailinput'}))
    password = CharField(label='Senha', widget=PasswordInput(attrs={'class': 'form-control',
        'placeholder': 'Senha',
        'id': 'passwordinput'}))


class AlterUserForm(UserChangeForm):

    use_required_attribute = False

    CHOICES = ((True, 'Vendedor'), (False, 'Comprador'))
    first_name = CharField(
        label='Primeiro nome',
        max_length=100,
        widget=TextInput(attrs={
            'class': 'form-control',
            'id': 'fnameInput',
            'placeholder': 'Primeiro Nome'
        }))
    last_name = CharField(
        label='Último nome',
        max_length=100,
        widget=TextInput(attrs={
            'class': 'form-control',
            'id': 'lnameInput',
            'placeholder': 'Último Nome'
        }))
    is_seller = ChoiceField(
        label='Status do usuário',
        choices=CHOICES,
        widget=Select(attrs={
            'class': 'form-control',
            'id': 'statusUser',
            'placehpçder': 'Status'
        }))

    class Meta:
        model = UserModel
        fields = 'first_name', 'last_name', 'is_seller'