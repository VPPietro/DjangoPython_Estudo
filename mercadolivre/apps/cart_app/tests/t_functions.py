from django.contrib.auth.models import AnonymousUser
from django.core.handlers.wsgi import WSGIRequest
from django.test import RequestFactory
from django.urls.base import reverse_lazy

from apps.loja_app.models import ItensModel
from apps.user_app.models import UserModel
from apps.cart_app.models import CartModel, CartItemModel


def set_request(self, url, user=None, post=False) -> WSGIRequest:
    """Retorna uma request get caso GET seja True se não uma request POST"""
    factory = RequestFactory()
    request = factory.post(url) if post else factory.get(url)
    request.session = self.client.session
    request.user = user if user else AnonymousUser()
    return request


def setup_std(self, user=False, anonimo=False, user_sem_carrinho=False):
    if user:
        self.user = UserModel.objects.create(
            email = 'user@gmail.com',
            username = 'UserCarrinho',
            first_name = 'User',
            last_name = 'Carrinho',
            password = 'toor',
            is_seller = True,)
        self.item_user = ItensModel.objects.create(
            nome = 'ItemTest1',
            descricao = 'este e o primeiro item',
            valor = 250,
            quantidade = 20,
            vendedor = self.user)
        self.item_user2 = ItensModel.objects.create(
            nome = 'ItemTest2',
            descricao = 'este e o segundo item',
            valor = 300,
            quantidade = 10,
            vendedor = self.user)
        self.item_carrinho_user = CartItemModel.objects.create(
            loja_item = self.item_user,
            quantidade_compra = 333)
        self.carrinho_do_user = CartModel.objects.create(
            comprador = self.user)
        self.carrinho_do_user.cart_item.add(self.item_carrinho_user)
    self.user_sem_carrinho = UserModel.objects.create(
            email = 'usersemcarrinho@gmail.com',
            username = 'UserSemCarrinho',
            first_name = 'User',
            last_name = 'Sem Carrinho',
            password = 'toor',
            is_seller = True,) if user_sem_carrinho else None
    if anonimo:
        self.item_carrinho_anonimo = CartItemModel.objects.create(
            loja_item = self.item_user,
            quantidade_compra = 666)
        self.item_carrinho_anonimo2 = CartItemModel.objects.create(
            loja_item = self.item_user2,
            quantidade_compra = 22)
        self.carrinho_anonimo = CartModel.objects.create()
        self.carrinho_anonimo.cart_item.add(self.item_carrinho_anonimo)
