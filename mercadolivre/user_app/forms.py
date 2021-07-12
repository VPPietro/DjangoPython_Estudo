from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, PasswordInput, Form
from django.forms.fields import EmailField
from .models import UserModel


class SignUpForm(UserCreationForm):

    def __init__(self, *args: any, **kwargs: any) -> None:
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = UserModel
        fields = 'username', 'email', 'first_name', 'last_name'


class LoginForm(Form):
    username = CharField(label='Username')
    password = CharField(label='Senha', widget=PasswordInput)


class AlterUserForm(Form):
    nome = CharField(label='Nome')
    sobrenome = CharField(label='Sobrenome')
    email = EmailField(label='E-mail')
    senha = CharField(label='Confirme sua senha', widget=PasswordInput)
