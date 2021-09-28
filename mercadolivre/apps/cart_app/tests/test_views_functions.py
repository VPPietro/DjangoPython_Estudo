from django.test import TestCase

from apps.cart_app.tests.t_functions import *
from apps.cart_app.views_functions import *


class get_or_create_cartTest(TestCase):
    def setUp(self) -> None:
        setup_std(self, user=True, anonimo=True)

    def tes_request_com_somente_cart_anonimo(self):
        """Verifica se a função retorna False e obj cart_anonimo"""
        # define uma request somente com cart anonimo
        request = set_request(self, reverse_lazy('cart_page'))
        request.session['anonimo'] = self.carrinho_anonimo.id
        # manda para a função
        retorno = get_or_create_cart(request)
        # verifica se retorna False, obj cart_anonimo
        self.assertEqual(not retorno[0], isinstance(retorno[1], CartModel))

    def tes_request_com_somente_cart_user(self):
        """Verifica se a função retorna obj cart_user e False"""
        # define uma request somente com cart user
        request = set_request(self, reverse_lazy('cart_page'), user=self.user)
        # manda para a função
        retorno = get_or_create_cart(request)
        # verifica se retorna obj cart_user e False
        self.assertEqual(isinstance(retorno[0], CartModel), not retorno[1])

    def tes_request_com_os_dois_carts(self):
        """Verifica se a função retorna obj cart_user e obj cart_anonimo"""
        # define uma request com os dois carts
        request = set_request(self, reverse_lazy('cart_page'), user=self.user)
        request.session['anonimo'] = self.carrinho_anonimo.id
        # manda para a função
        retorno = get_or_create_cart(request)
        # verifica se retorna obj cart_user e obj cart_anonimo
        self.assertEqual(isinstance(retorno[0], CartModel), isinstance(retorno[1], CartModel))


class get_cart_itemsTest(TestCase):

    def tes_manda_carrinho_com_itens(self):
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

    def tes_manda_carrinho_sem_itens(self):
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

    def tes_user_anonimo_com_carrinho(self):
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

    def tes_user_anonimo_sem_carrinho(self):
        """Verifica se a função retorna um novo carrinho para o user anonimo"""
        # define uma request com user anonimo e sem carrinho
        request = set_request(self, '')
        # manda para a função
        retorno = ajusta_carrinho(request)
        # verifica se retorna um novo carrinho para o user anonimo
        self.assertTrue(isinstance(retorno[1], CartModel))

    def tes_user_logado_sem_carrinho_anonimo(self):
        """Verifica se a função retorna o carrinho do user sem alterações"""
        # define uma request com user logado, sem carrinho anonimo
        request = set_request(self, '', user=self.user)
        # manda para a função
        retorno = ajusta_carrinho(request)
        # verifica se retorna o cart do user sem alterações
        self.assertEqual(retorno[0].cart_item.all()[0], self.carrinho_do_user.cart_item.all()[0])
        self.assertEqual(retorno[0].cart_item.all()[0].quantidade_compra, self.carrinho_do_user.cart_item.all()[0].quantidade_compra)

    def tes_user_logado_com_carrinho_anonimo(self):
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
    def setUp(self) -> None:
        return super().setUp()

    def t_cria_carrinho_anonimo(self):
        """Cria um carrinho sem um user, ou seja, anonimo"""
        # chama a função sem nenhum valor informado
        # verifica se é retornado um CartModel sem usuário
        pass

    def t_cria_carrinho_com_user(self):
        """Cria um carrinho com um user"""
        # chama a função informando um user
        # verifica se é retornado um CartModel com o usuário informado
        pass


class deleta_carrinhoTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def t_deleta_carrinho(self):
        """Verifica se a função deleta um carrinho"""
        # manda um carrinho para a função
        # verifica se o carrinho foi deletado
        pass


class join_cartsTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def t_manda_carrinho_vazio_anonimo_com_item(self):
        """Verifica se será adicionado os itens do cart anonimo para o cart do user"""
        # manda um carrinho vazio e um carrinho anonimo com item para a função
        # verifica se o carrinho anonimo ficou vazio (talvez precise definir a.delete() nos elifs (linhas 66 e 68))
        # verifica se o carrinho user esta com os itens
        pass

    def t_manda_carrinho_com_item_anonimo_vazio(self):
        """A função não deve fazer nada, pois não é necessário alterar"""
        # manda um carrinho com itens e um carrinho anonimo vazio para a função
        # verifica se nenhuma alteração foi feita
        pass

    def t_manda_todos_carrinhos_com_itens(self):
        """Verifica se será adicionado os itens do cart anonimo para o cart do user"""
        # manda um carrinho com um iten x e um carrinho anonimo com iten x e y para a função
        # verifica se o carrinho anonimo ficou vazio (talvez precise definir a.delete() nos elifs (linhas 66 e 68))
        # verifica se o carrinho user esta com os itens x + 1 e y
        pass


class add_to_cart_funcTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def t_manda_item_existente_no_carrinho(self):
        """Verifica se ao mandar um item que já existe no carrinho
        o mesmo não será duplicado, mas sim, terá sua quantidade aumentada"""
        # manda um id de um item que já esta no carrinho
        # verifica se a quantidade do item aumentou
        # verifica se o item não foi duplicado
        pass

    def t_manda_item_inexistente_no_carrinho(self):
        """Verifica se ao mandar um item que não existe no carrinho, é criado um novo"""
        # manda um id de um item que não está no carrinho
        # verifica se o item foi adicionado
        # verifica se o item não foi duplicado
        pass
