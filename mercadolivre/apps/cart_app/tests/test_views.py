from django.http.response import Http404
from django.test import TestCase

from apps.cart_app.tests.t_functions import *
from apps.cart_app.views import CartView, RemoveFromCart, add_to_cart



class CartViewTest(TestCase):
    def setUp(self) -> None:
        setup_std(self, user=True, anonimo=True, user_sem_carrinho=True)

    def test_user_logado_sem_cart_anonimo(self):
        """Verifica se quando acessado a página de carrinho, sem carrinho anonimo,
        o usuario logado recebe o seu carrinho do db"""
        # seta o user que já tem um carrinho para a request
        request = set_request(self, url=reverse_lazy('cart_page'), user=self.user)
        self.assertTrue(request.user.is_authenticated)
        # manda a request get para CartView
        retorno = CartView.as_view()(request)
        # verifica se o carrinho que já existia foi mostrado
        obj_cartitemmodel_retorno = retorno.context_data['itens'][0]
        self.assertEqual(obj_cartitemmodel_retorno.id, self.item_carrinho_user.id)
        self.assertEqual(obj_cartitemmodel_retorno.quantidade_compra, 333)

    def test_user_logado_com_cart_anonimo(self):
        """Verifica se quando acessado a página de carrinho, com carrinho anonimo,
        o usuário logado recebe seu carrinho unificado com o anonimo"""
        # seta user que já tem um carrinho para a request
        request = set_request(self, reverse_lazy('cart_page'), user=self.user)
        # seta um carrinho anonimo para a request
        request.session['anonimo'] = self.carrinho_anonimo.id
        # manda a request para CartView
        retorno = CartView.as_view()(request)
        obj_cartitemmodel_retorno = retorno.context_data['itens']
        # verifica se o carrinho retornado é do user
        self.assertTrue(CartModel.objects.filter(cart_item=obj_cartitemmodel_retorno[0].id))
        # verifica se os itens originais do user foram acrescidos dos itens do carrinho anonimo
        self.assertEqual(obj_cartitemmodel_retorno[0].quantidade_compra,
            self.item_carrinho_anonimo.quantidade_compra + self.item_carrinho_user.quantidade_compra)
        # verifica se o carrinho anonimo foi removido da db
        carrinho_anonimo_db = CartModel.objects.filter(id=self.carrinho_anonimo.id)
        self.assertFalse(carrinho_anonimo_db)

    def test_user_logado_sem_nenhum_carrinho(self):
        """Verifica se quando um novo usuario loga no site e acessa página de carrinho,
        é criado um novo cart"""
        # seta um user sem carrinho para a request
        request = set_request(self, reverse_lazy('cart_page'), user=self.user_sem_carrinho)
        # manda a request para CartView
        CartView.as_view()(request)
        novo_carrinho = CartModel.objects.filter(comprador=self.user_sem_carrinho.id)
        # verifica se foi criado um carrinho para o user
        self.assertTrue(novo_carrinho)


class RemoveFromCartTest(TestCase):
    def setUp(self) -> None:
        setup_std(self, user=True, user_sem_carrinho=True)
        self.request = set_request(self, 'cart/remove_from_cart', self.user)

    def test_exclui_item_do_carrinho(self):
        """Verifica se ao mandar a request com a pk do produto do carrinho
        o item é excluido do carrinho"""
        # manda uma request get (a view esta configurada para dar post ao receber get) para RemoveFromCart
        RemoveFromCart.as_view()(self.request, pk=self.item_carrinho_user.id)
        retorno = CartView.as_view()(self.request)
        # verifica se o item foi excluido do carrinho
        self.assertFalse(retorno.context_data['itens'])

    def test_tenta_excluir_item_que_nao_tem_no_carrinho(self):
        """Verifica se ao mandar uma request com a pk incorreta de um CartItem inexistente
        retorna um 404"""
        # manda uma request get para RemoveFromCart
        try: RemoveFromCart.as_view()(self.request, pk=999)
        except Http404: self.assertTrue(True)
        except: self.assertTrue(False)


class add_to_cartTest(TestCase):
    def setUp(self) -> None:
        setup_std(self, user=True, user_sem_carrinho=True)
        self.request_anonimo = set_request(self, 'cart/add_to_cart/')

    def test_adiciona_item_sem_ter_carrinho_anonimo(self):
        """Verifica se um user anonimo consegue adicionar item sem ter criado um carrinho ainda
        (deve ser criado um automaticamente)"""
        # com user anonimo e sem carrinho, manda uma request para add_to_cart com o pk do item à adicionar
        add_to_cart(self.request_anonimo, pk=self.item_user.id)
        cart_anonimo = self.request_anonimo.session.get('anonimo', False)
        if cart_anonimo: cart_anonimo = CartModel.objects.get(id=cart_anonimo)
        # verifica se foi criado um cart anonimo
        self.assertTrue(cart_anonimo)
        # verifica se foi adicionado o item para o cart anonimo
        self.assertTrue(cart_anonimo.cart_item.all())

    def test_adiciona_item_ja_tendo_carrinho_anonimo(self):
        """Verifica se um user anonimo que já possui carrinho anonimo consegue adicionar
        itens no seu carrinho"""
        self.request_anonimo.session['anonimo'] = self.carrinho_do_user.id
        # com user anonimo e com carrinho, manda uma request para add_to_cart com o pk do item à adicionar
        add_to_cart(self.request_anonimo, pk=self.item_user.id)
        # verifica se foi adicionado o item para o cart anonimo
        cart_anonimo = CartModel.objects.get(id=self.request_anonimo.session.get('anonimo'))
        self.assertEqual(cart_anonimo.cart_item.all()[0].quantidade_compra,
            self.item_carrinho_user.quantidade_compra + 1)

    def test_adiciona_item_sem_ter_carrinho_user(self):
        """Verifica se um user logado que ainda não possui carrinho, consegue adicionar item
        e criar carrinho automaticamente"""
        request_user = set_request(self, 'cart/add_to_cart/', user=self.user_sem_carrinho)
        # com um user logado e sem carrinho, manda uma request para add_to_cart com o pk do item à adicionar
        add_to_cart(request_user, pk=self.item_user.id)
        cart_user = CartModel.objects.filter(comprador=self.user_sem_carrinho.id)
        # verifica se foi criado um carrinho para o user
        self.assertTrue(cart_user)
        # verifica se o item foi adicionado para o carrinho do user
        self.assertTrue(cart_user[0].cart_item.all())

    def test_adiciona_item_ja_tendo_carrinho_user(self):
        """Verifica se um user logado que já possui carrinho consegue adicionar item ao cart"""
        request_user = set_request(self, 'cart/add_to_cart/', user=self.user)
        # com um user logado e com carrinho, manda uma request para add_to_cart com o pk do item à adicionar
        add_to_cart(request_user, pk=self.item_user.id)
        # verifica se foi adicionado no carrinho do user
        self.assertEqual(self.carrinho_do_user.cart_item.all()[0].quantidade_compra,
            self.item_carrinho_user.quantidade_compra + 1)



"""Remover criacao de users de setup, já que nem todos os users são usados em todos os testes"""