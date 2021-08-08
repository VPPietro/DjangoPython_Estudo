from apps.user_app.models import UserModel
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.conf import settings
from django.views.generic.edit import CreateView
from .forms import AlterUserForm, SignUpForm, LoginForm


class LoginClassView(LoginView):  # Criar mensagens de erro ou falhas
    template_name = 'user/login_page.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True
    settings.LOGIN_REDIRECT_URL = reverse_lazy('lista-itens-user')


class SignUpClassView(CreateView):  # Remover mensagem 'User model com este E-mail já existe.'
    model = UserModel
    template_name = 'user/signup_page.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login_page')


def signup(request):
    usuario = get_user(request)
    form = SignUpForm()
    if usuario.is_anonymous:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(request, email=user.email, password=raw_password)
                if user is not None:
                    login(request, user)
                else:
                    messages.error(request, 'Ocorreu um erro, tente fazer login')
                return redirect('index_page')
            else:
                messages.error(request, 'Formulário preenchido incorretamente, favor corrigir os campos destacados')
        else:
            form = SignUpForm()
    return render(request, 'user/signup_page.html', {'form': form})


def logoff_view(request):
    logout(request)
    return redirect('index_page')


def user_info_view(request):
    if request.user.is_anonymous:
        return redirect('/user/login')
    else:
        if request.method == 'POST':
            form = AlterUserForm(request.POST)
            return render(request, 'user/login', {'form': form})
        return render(request, 'user/user_page.html')


def alter_user_info_view(request):
    usuario = get_user(request)
    if usuario.is_anonymous:
        return redirect('/user/login')
    form = AlterUserForm(initial={
        'nome': usuario.get_first_name(),
        'sobrenome': usuario.get_last_name(),
        'email': usuario.get_email(),
        })
    if request.method == 'POST':
        senha = request.POST['senha']
        authent = authenticate(request, username=usuario.get_username(), password=senha)
        if authent is not None:
            usuario.set_first_name(request.POST['nome'])
            usuario.set_last_name(request.POST['sobrenome'])
            usuario.set_email(request.POST['email'])
            return redirect('user_info_page')
        else:
            messages.error(request, 'Senha incorreta')
    return render(request, 'user/alter_user_page.html', {'form': form})
