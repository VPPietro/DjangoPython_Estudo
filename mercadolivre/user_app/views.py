from django.shortcuts import redirect, render
from .forms import SignInForm, LoginForm
from django.contrib.auth import authenticate, get_user, login, logout
from django.contrib.auth.models import User


def login_view(request):
    form = LoginForm()
    usuario = get_user(request)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form['username'].value(), password=form['password'].value())
            print('login of ', user)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                print('login user dosent existis/invalid') # definir retorno de usuario inexistente na pag.
    return render(request, 'login_page.html', {'form': form, 'usuario': usuario})

def signin_view(request):
    usuario = get_user(request)
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignInForm()
    return render(request, 'signin_page.html', {'form': form, 'usuario': usuario})

def logoff_view(request):
    logout(request)
    return redirect('/index/')

def user_info_view(request):
    usuario = get_user(request)
    if usuario.is_anonymous:
        return redirect('/user/login')
    nome = usuario.get_full_name()
    email = User.objects.filter(username=usuario).values('email')[0]['email']
    data_cadastro = User.objects.filter(username=usuario).values('date_joined')[0]['date_joined']
    ultimo_login = User.objects.filter(username=usuario).values('last_login')[0]['last_login']
    return render(request, 'user_page.html', 
        {'usuario': usuario,
         'nome': nome.title(), 
         'email': email,
         'data_cadastro': data_cadastro,
         'senha': '*******',
         'ultimo_login': ultimo_login,
         })

def alter_user_info_view(request):
    usuario = get_user(request)
    nome = usuario.get_full_name()
    email = User.objects.filter(username=usuario).values('email')[0]['email']
    return render(request, 'alter_user_page.html', 
        {'usuario': usuario,
         'nome': nome.title(), 
         'email': email,
         'senha': '*******',
         })
