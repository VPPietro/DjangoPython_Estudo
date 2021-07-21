from django.contrib.auth import authenticate, login, logout, get_user
from django.shortcuts import redirect, render
from .forms import AlterUserForm, SignUpForm, LoginForm
from django.views.generic.detail import DetailView


def login_view(request):
    form = LoginForm()
    usuario = get_user(request)
    if usuario.is_anonymous:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            print(form)
            if form.is_valid():
                user = authenticate(request, username=form['username'].value(), password=form['password'].value())
                print('login of ', user)
                if user is not None:
                    login(request, user)
                    return redirect('/')
                else:
                    print('login user dosent existis/invalid') # definir retorno de usuario inexistente na pag.
    return render(request, 'user/login_page.html', {'form': form})


def signup(request):
    usuario = get_user(request)
    form = SignUpForm()
    if usuario.is_anonymous:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            print(form)
            if form.is_valid():
                user = form.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(request, email=user.email, password=raw_password)
                if user is not None:
                    login(request, user)
                else:
                    print('usuario nao encontrado')
                return redirect('index_page')
            else:
                print('formulario incorreto')
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
    login_erro = False
    if request.method == 'POST':
        senha = request.POST['senha']
        authent = authenticate(request, username=usuario.get_username(), password=senha)
        if authent is not None:
            usuario.set_first_name(request.POST['nome'])
            usuario.set_last_name(request.POST['sobrenome'])
            usuario.set_email(request.POST['email'])
            return redirect('/')
        else:
            login_erro = True
    return render(request, 'user/alter_user_page.html', {'form': form, 'login_erro': login_erro})
