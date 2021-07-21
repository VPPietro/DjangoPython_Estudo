from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, PasswordInput, Form
from django.forms.fields import EmailField
from .models import UserModel


class SignUpForm(UserCreationForm):

    def __init__(self, *args: any, **kwargs: any) -> None:
        super().__init__(*args, **kwargs)
        # Remove help text:
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = UserModel
        fields = 'username', 'email', 'first_name', 'last_name'


class LoginForm(Form):
    username = CharField(label='Username')
    password = CharField(label='Senha', widget=PasswordInput)
    # name = CharField(widget=TextInput(attrs={"class": "form-control"}))
    # message = CharField(widget=Textarea(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'nome@dominio.com.br'
        self.fields['username'].widget.attrs['id'] = 'floatingInput'

        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Senha'
        self.fields['password'].widget.attrs['id'] = 'floatingPassword'
        print(self.fields.items())  

class AlterUserForm(Form):
    nome = CharField(label='Nome')
    sobrenome = CharField(label='Sobrenome')
    email = EmailField(label='E-mail')
    senha = CharField(label='Confirme sua senha', widget=PasswordInput)
