from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from django.http.response import HttpResponseBase, HttpResponseRedirect, HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.conf import settings
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView

from apps.user_app.forms import AlterUserForm, SignUpForm, LoginForm
from apps.user_app.models import UserModel
from apps.cart_app.models import CartModel
from apps.cart_app.functions import join_carts

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

    # def post(self, request: HttpRequest, *args: str, **kwargs: any) -> HttpResponse:
    #     carrinho_anonimo = self.request.session.get('carrinho', False)
    #     if carrinho_anonimo and get_cart_items(request):
    #         request.session['carrinho_anonimo'] = carrinho_anonimo
    #     return super().post(request, *args, **kwargs)


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

    def get_object(self):
        """Por padrão o DetailView precisa de um 'pk' na URL, sobrescrevendo este método,
        a página 'user info' sempre mostrará somente as informações do user logado"""
        return get_object_or_404(UserModel, pk=self.request.user.id)


@method_decorator(decorator_login, 'dispatch')
class UpdateUserInfoClassView(UpdateView):
    model = UserModel
    template_name = 'user/alter_user_page.html'
    form_class = AlterUserForm
    success_url = reverse_lazy('user_info_page')

    def get_object(self):
        """Por padrão o DetailView precisa de um 'pk' na URL, sobrescrevendo este método,
        a página 'user info' sempre mostrará somente as informações do user logado"""
        return get_object_or_404(UserModel, pk=self.request.user.id)
