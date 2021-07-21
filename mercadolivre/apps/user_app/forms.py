from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, PasswordInput, Form, EmailField, EmailInput
from .models import UserModel


class SignUpForm(UserCreationForm):
    def __init__(self, *args: any, **kwargs: any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['id'] = 'floatingInput'

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['id'] = 'floatingInput'

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['id'] = 'floatingInput'

        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['id'] = 'floatingInput'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['id'] = 'passwordInput'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['id'] = 'passwordInput'

        # Remove help text:
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = UserModel
        fields = 'username', 'email', 'first_name', 'last_name'


class LoginForm(Form):
    username = EmailField(label='Username', widget=EmailInput(attrs=
                                                              {'class': 'form-control',
                                                               'placeholder': 'nome@dominio.com.br',
                                                               'id': 'floatingInput'}))
    password = CharField(label='Senha', widget=PasswordInput(attrs=
                                                             {'class': 'form-control',
                                                              'placeholder': 'Senha',
                                                              'id': 'floatingPassword'}))


class AlterUserForm(Form):
    nome = CharField(label='Nome')
    sobrenome = CharField(label='Sobrenome')
    email = EmailField(label='E-mail')
    senha = CharField(label='Confirme sua senha', widget=PasswordInput)
