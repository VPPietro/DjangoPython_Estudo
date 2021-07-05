from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import CharField, PasswordInput, Form


class SignInForm(UserCreationForm):

    def __init__(self, *args: any, **kwargs: any) -> None:
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = 'username','first_name', 'last_name', 'email'


class LoginForm(Form):
    username = CharField(label='Username')
    password = CharField(label='Senha', widget=PasswordInput)
