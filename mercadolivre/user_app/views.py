from django.contrib.auth import authenticate, login, logout, get_user
from django.shortcuts import redirect, render
from .forms import AlterUserForm, SignUpForm, LoginForm
from django.views.generic.detail import DetailView

class UserView(DetailView):

    template_name = 'sigin_page.html'


    def get_object(self):
        return self.request.user

def login_view(request):
    form = LoginForm()
    usuario = get_user(request)
    superuser = False
    if str(usuario) != 'AnonymousUser':
        superuser = usuario.get_is_superuser()
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
    return render(request, 'login_page.html',
        {'form': form,
        'usuario': usuario,
        'superuser': superuser
        })

def signup(request):
    usuario = get_user(request)
    superuser = False
    if str(usuario) != 'AnonymousUser':
        superuser = usuario.get_is_superuser()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, email=user.email, password=raw_password)
            if user is not None:
                login(request, user)
            else:
                print('usuario nao encontrado')
            return redirect('/')
        else:
            print('formulario incorreto')
    else:
        form = SignUpForm()
    return render(request, 'signup_page.html',
        {'form': form,
        'usuario': usuario,
        'superuser': superuser
        })

def logoff_view(request):
    logout(request)
    return redirect('/index/')

def user_info_view(request):
    usuario = get_user(request)

    superuser = False
    if str(usuario) != 'AnonymousUser':
        superuser = usuario.get_is_superuser()
    return render(request, 'user_page.html',
        {'usuario': usuario,
        'superuser': superuser,
        'nome' : usuario.get_full_name(),
        'email': usuario.get_email(),
        'data_cadastro': usuario.get_data_cadastro(),
        })

def alter_user_info_view(request):
    usuario = get_user(request)
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
        else:
            login_erro = True
    return render(request, 'alter_user_page.html', {'form': form,'usuario': usuario, 'login_erro': login_erro})
