from django.contrib.auth import authenticate, login, logout, get_user
from django.shortcuts import redirect, render
from .forms import AlterUserForm, SignUpForm, LoginForm
from .models import UserModel
from django.views.generic.detail import DetailView

class UserView(DetailView):

    template_name = 'sigin_page.html'

    def get_object(self):
        return self.request.user

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

def signup(request):
    usuario = get_user(request)
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
    return render(request, 'signup_page.html', {'form': form, 'usuario': usuario})

def logoff_view(request):
    logout(request)
    return redirect('/index/')


def user_info_view(request):
    usuario = get_user(request)


    return render(request, 'user_page.html', {'usuario': usuario})