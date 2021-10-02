from django.test import TestCase

from apps.cart_app.tests.t_functions import *
from apps.cart_app.views_functions import *

"""Remover test de ajustar carrinho? já que são os testes de get_or_create_cart e join_cart juntos"""


class get_or_create_cartTest(TestCase):
    def setUp(self) -> None:
        setup_std(self, user=True, anonimo=True)

    def test_request_com_somente_cart_anonimo(self):
        """Verifica se a função retorna False e obj cart_anonimo"""
        # define uma request somente com cart anonimo
        request = set_request(self, reverse_lazy('cart_page'))
        request.session['anonimo'] = self.carrinho_anonimo.id
        # manda para a função
        retorno = get_or_create_cart(request)
        # verifica se retorna False, obj cart_anonimo
        self.assertEqual(not retorno[0], isinstance(retorno[1], CartModel))

    def test_request_com_somente_cart_user(self):
        """Verifica se a função retorna obj cart_user e False"""
        # define uma request somente com cart user
        request = set_request(self, reverse_lazy('cart_page'), user=self.user)
        # manda para a função
        retorno = get_or_create_cart(request)
        # verifica se retorna obj cart_user e False
        self.assertEqual(isinstance(retorno[0], CartModel), not retorno[1])

    def test_request_com_os_dois_carts(self):
        """Verifica se a função retorna obj cart_user e obj cart_anonimo"""
        # define uma request com os dois carts
        request = set_request(self, reverse_lazy('cart_page'), user=self.user)
        request.session['anonimo'] = self.carrinho_anonimo.id
        # manda para a função
        retorno = get_or_create_cart(request)
        # verifica se retorna obj cart_user e obj cart_anonimo
        self.assertEqual(isinstance(retorno[0], CartModel), isinstance(retorno[1], CartModel))


class get_cart_itemsTest(TestCase):

    def test_manda_carrinho_com_itens(self):
        """Verifica se ao mandar carrinho com itens, é retornado um queryset
        com cart_items"""
        # cria um carrinho com itens
        setup_std(self, user=True)
        # manda o carrinho para a função
        retorno = get_cart_items(self.carrinho_do_user)
        # verifica se retornou queryset com os cart_items
        self.assertTrue(isinstance(retorno, QuerySet))
        # verifica se retornou o item dentro do queryset(queryset vazio retorna False)
        self.assertTrue(retorno)

    def test_manda_carrinho_sem_itens(self):
        """Verifica se ao mandar carrinho sem itens, é retornado um queryset vazio"""
        # cria um carrinho sem itens
        carrinho = CartModel.objects.create()
        # manda o carrinho para a função
        retorno = get_cart_items(carrinho)
        # verifica se retornou queryset vazio
        self.assertFalse(retorno)


class ajusta_carrinhoTest(TestCase):
    def setUp(self) -> None:
        setup_std(self, user=True, anonimo=True)

    def test_user_anonimo_com_carrinho(self):
        """Verifica se a função retorna o carrinho do user anonimo sem alterações"""
        # define uma request com user anonimo com carrinho
        request = set_request(self, '')
        request.session['anonimo'] = self.carrinho_anonimo.id
        # manda para a função
        retorno = ajusta_carrinho(request)
        # verifica se retorna (False, carrinho)
        self.assertEqual(not retorno[0], isinstance(retorno[1], CartModel))
        # verifica se carrinho anonimo é retornado sem alterações
        self.assertEqual(retorno[1].cart_item.all()[0], self.carrinho_anonimo.cart_item.all()[0])
        self.assertEqual(retorno[1].cart_item.all()[0].quantidade_compra, self.carrinho_anonimo.cart_item.all()[0].quantidade_compra)

    def test_user_anonimo_sem_carrinho(self):
        """Verifica se a função retorna um novo carrinho para o user anonimo"""
        # define uma request com user anonimo e sem carrinho
        request = set_request(self, '')
        # manda para a função
        retorno = ajusta_carrinho(request)
        # verifica se retorna um novo carrinho para o user anonimo
        self.assertTrue(isinstance(retorno[1], CartModel))

    def test_user_logado_sem_carrinho_anonimo(self):
        """Verifica se a função retorna o carrinho do user sem alterações"""
        # define uma request com user logado, sem carrinho anonimo
        request = set_request(self, '', user=self.user)
        # manda para a função
        retorno = ajusta_carrinho(request)
        # verifica se retorna o cart do user sem alterações
        self.assertEqual(retorno[0].cart_item.all()[0], self.carrinho_do_user.cart_item.all()[0])
        self.assertEqual(retorno[0].cart_item.all()[0].quantidade_compra, self.carrinho_do_user.cart_item.all()[0].quantidade_compra)

    def test_user_logado_com_carrinho_anonimo(self):
        """Verifica se a função retorna o carrinho do user junto com os itens do carrinho anonimo"""
        # define uma request com user logado, com carrinho anonimo
        request = set_request(self, '', user=self.user)
        request.session['anonimo'] = self.carrinho_anonimo.id
        qnt_cart_user = self.carrinho_do_user.cart_item.all()[0].quantidade_compra
        qnt_cart_anonimo = self.carrinho_anonimo.cart_item.all()[0].quantidade_compra
        # manda para a função
        retorno = ajusta_carrinho(request)[0]
        # verifica se retorna o cart do user
        self.assertTrue(isinstance(retorno, CartModel))
        # verifica se os carrinhos são juntados
        qnt_cart_retorno = retorno.cart_item.all()[0].quantidade_compra
        self.assertEqual(qnt_cart_retorno, qnt_cart_user + qnt_cart_anonimo)


class cria_carrinhoTest(TestCase):

    def test_cria_carrinho_anonimo(self):
        """Cria um carrinho sem um user, ou seja, anonimo"""
        # chama a função sem nenhum valor informado
        retorno = cria_carrinho()
        # verifica se é retornado um CartModel sem usuário
        self.assertTrue(isinstance(retorno, CartModel))

    def test_cria_carrinho_com_user(self):
        """Cria um carrinho com um user"""
        setup_std(self, user_sem_carrinho=True)
        # chama a função informando um user
        retorno = cria_carrinho(user=self.user_sem_carrinho)
        # verifica se é retornado um CartModel com o usuário informado
        self.assertTrue(isinstance(retorno, CartModel))


class deleta_carrinhoTest(TestCase):
    def setUp(self) -> None:
        setup_std(self, user=True)

    def test_deleta_carrinho(self):
        """Verifica se a função deleta um carrinho"""
        # manda um carrinho para a função
        deleta_carrinho(self.carrinho_do_user)
        # verifica se o carrinho foi deletado
        self.assertFalse(self.carrinho_do_user.id)


class join_cartsTest(TestCase):
    def setUp(self) -> None:
        setup_std(self, user=True,anonimo=True)

    def test_manda_carrinho_user_vazio_e_anonimo_com_item(self):
        """Verifica se será adicionado os itens do cart anonimo para o cart do user"""
        # manda um carrinho vazio e um carrinho anonimo com item para a função
        carrinho_user = CartModel.objects.create()
        join_carts(carrinho_user, self.carrinho_anonimo)
        # verifica se o carrinho user esta com os itens
        item_user = carrinho_user.cart_item.all()[0]
        item_anonimo = carrinho_user.cart_item.all()[0]
        self.assertEqual(item_user.loja_item.id, item_anonimo.loja_item.id)
        self.assertEqual(item_user.quantidade_compra, item_anonimo.quantidade_compra)

    def test_manda_carrinho_do_user_com_item_e_anonimo_vazio(self):
        """A função não deve fazer nada, pois não é necessário alterar"""
        # manda um carrinho com itens e um carrinho anonimo vazio para a função
        carrinho_anonimo = CartModel.objects.create()
        item_original = self.carrinho_do_user.cart_item.all()[0]
        join_carts(self.carrinho_do_user, carrinho_anonimo)
        item_pos_join = self.carrinho_do_user.cart_item.all()[0]
        # verifica se nenhuma alteração foi feita
        self.assertEqual(item_original.loja_item.id, item_pos_join.loja_item.id)
        self.assertEqual(item_original.quantidade_compra, item_pos_join.quantidade_compra)

    def test_manda_todos_carrinhos_com_itens(self):
        """Verifica se será adicionado os itens do cart anonimo para o cart do user"""
        # verifica se o user só tem um item inicialmente no carrinho
        itens_user_original = self.carrinho_do_user.cart_item.all()
        self.assertEqual(len(itens_user_original), 1)
        # manda um carrinho com um iten x e um carrinho anonimo com iten x e y para a função
        self.carrinho_anonimo.cart_item.add(self.item_carrinho_anonimo2)
        itens_anonimo = list(self.carrinho_anonimo.cart_item.all())
        join_carts(self.carrinho_do_user, self.carrinho_anonimo)
        # verifica se o carrinho user esta com os itens x_user + x_anonimo e y
        itens_user = self.carrinho_do_user.cart_item.all()
        self.assertEqual(len(itens_user), 2)
        self.assertEqual(itens_user[0].quantidade_compra, itens_user_original[0].quantidade_compra + itens_anonimo[0].quantidade_compra)
        self.assertEqual(itens_user[1].loja_item.id, itens_anonimo[1].loja_item.id)


class add_to_cart_funcTest(TestCase):
    def setUp(self) -> None:
        setup_std(self, user=True)
        self.itens_carrinho = self.carrinho_do_user.cart_item.all()

    def test_manda_item_existente_no_carrinho(self):
        """Verifica se ao mandar um item que já existe no carrinho
        o mesmo não será duplicado, mas sim, terá sua quantidade aumentada"""
        self.assertEqual(self.itens_carrinho[0].quantidade_compra, 333)
        # manda um id de um item que já esta no carrinho
        add_to_cart_func(self.item_user.id, self.carrinho_do_user)
        self.itens_carrinho = self.carrinho_do_user.cart_item.all()
        # verifica se a quantidade do item aumentou
        self.assertEqual(self.itens_carrinho[0].quantidade_compra, 334)
        # verifica se o item não foi duplicado
        self.assertEqual(len(self.itens_carrinho), 1)

    def test_manda_item_inexistente_no_carrinho(self):
        """Verifica se ao mandar um item que não existe no carrinho, é criado um novo"""
        # manda um id de um item que não está no carrinho
        add_to_cart_func(self.item_user2.id, self.carrinho_do_user)
        self.itens_carrinho = self.carrinho_do_user.cart_item.all()
        # verifica se o item não foi duplicado
        self.assertEqual(len(self.itens_carrinho), 2)
        # verifica se o item correto foi adicionado
        self.assertEqual(self.itens_carrinho[1].loja_item.id, self.item_user2.id)
        self.assertEqual(self.itens_carrinho[1].quantidade_compra, 1)
