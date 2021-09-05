from django.http import HttpRequest
from django.http.response import HttpResponseBase, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView, LogoutView, redirect_to_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.conf import settings
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from apps.user_app.forms import AlterUserForm, SignUpForm, LoginForm
from apps.user_app.models import UserModel

decorator_login = [
    login_required(login_url='/user/login')
    ]


class LoginClassView(LoginView):  # Criar mensagens de erro ou falhas
    template_name = 'user/login_page.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True
    settings.LOGIN_REDIRECT_URL = reverse_lazy('lista-itens-user')

    def dispatch(self, request: HttpRequest, *args: any, **kwargs: any) -> HttpResponseBase:
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        messages.error(self.request, 'Email ou senha inválido(s), tente novamente')
        return super().form_invalid(form)


class SignUpClassView(CreateView):
    model = UserModel
    template_name = 'user/signup_page.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login_page')
    success_message = 'Cadastro realizado com sucesso!'
    redirect_authenticated_user = True

    def dispatch(self, request: HttpRequest, *args: any, **kwargs: any) -> HttpResponseBase:
        """Redireciona o usuario para a página de 'sua loja' caso o mesmo já esteja logado"""
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = reverse_lazy('lista-itens-user')
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro no cadastro, corrija os erros e tente novamente!')
        return super().form_invalid(form)


@method_decorator(decorator_login, 'dispatch')
class SignOutClassView(LogoutView):
    settings.LOGOUT_REDIRECT_URL = reverse_lazy('index_page')


@method_decorator(decorator_login, 'dispatch')
class InfoUserClassView(DetailView):
    model = UserModel
    template_name = 'user/user_page.html'
    context_object_name = 'user'


class UpdateUserInfoClassView(UpdateView):
    model = UserModel
    template_name = 'user/alter_user_page.html'
    form_class = AlterUserForm

    def get_initial(self):
        usuario = self.request.user
        self.initial['first_name'] = usuario.first_name
        self.initial['last_name'] = usuario.last_name
        self.initial['email'] = usuario.email
        self.initial['is_seller'] = [True if usuario.is_seller else False]
        return super().get_initial()

    def get_success_url(self) -> str:
        user_id = self.kwargs['pk']
        return reverse_lazy('user_info_page', kwargs={'pk': user_id})
