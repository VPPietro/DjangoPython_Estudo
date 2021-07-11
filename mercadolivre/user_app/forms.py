from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, PasswordInput, Form
from django.forms.fields import EmailField
from .models import UserModel


class SignUpForm(UserCreationForm):

    class Meta:
        model = UserModel
        fields = 'username', 'email'


class LoginForm(Form):
    username = CharField(label='Username')
    password = CharField(label='Senha', widget=PasswordInput)


class AlterUserForm(Form):
    nome = CharField(label='Nome')
    email = EmailField(label='E-mail')
    senha = CharField(label='Confirme sua senha', widget=PasswordInput)
