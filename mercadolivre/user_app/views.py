from django.shortcuts import redirect, render
from .forms import SignInForm, LoginForm
from django.contrib.auth import authenticate, get_user, login, logout


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
                print('login user dosent existis/invalid')
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
    usuario = get_user(request)
    logout(request)
    return render(request, 'logoff_page.html', {'usuario': usuario})
