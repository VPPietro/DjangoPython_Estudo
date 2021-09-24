from django.test import TestCase, RequestFactory
from django.urls import reverse_lazy

from apps.loja_app.models import ItensModel
from apps.user_app.models import UserModel
from apps.cart_app.models import CartModel, CartItemModel
from apps.cart_app.views import CartView


class CartViewTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
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
        self.item_carrinho_user = CartItemModel.objects.create(
            loja_item = self.item_user,
            quantidade_compra = 2)
        self.carrinho_do_user = CartModel.objects.create(
            comprador = self.user)

    def test_user_logado_sem_cart_anonimo(self):
        """Verifica se quando acessado a página de carrinho, sem carrinho anonimo,
        o usuario logado recebe o seu carrinho do db"""
        # seta o user que já tem um carrinho para a request
        request = self.factory.get(reverse_lazy('cart_page'))
        request.session = self.client.session
        request.user = self.user
        self.assertTrue(request.user.is_authenticated)
        # manda a request get para CartView
        retorno = CartView.as_view()(request)
        # verifica se o carrinho que já existia foi mostrado
        print(retorno)

    def t_user_logado_com_cart_anonimo(self):
        """Verifica se quando acessado a página de carrinho, com carrinho anonimo,
        o usuário logado recebe seu carrinho unificado com o anonimo"""
        # seta user que já tem um carrinho para a request
        # seta um carrinho anonimo para a request em request.session['anonimo']
        # manda a request para CartView
        # verifica se os itens originais do user foi acrescido dos itens do carrinho anonimo
        pass

    def t_user_logado_sem_nenhum_carrinho(self):
        """Verifica se quando um novo usuario loga no site e acessa página de carrinho,
        se é criado um novo cart"""
        # seta um user sem carrinho para a request
        # manda a request para CartView
        # verifica se foi criado um carrinho para o user
        pass

    def t_verifica_se_tem_itens_duplicados(self):
        """Verifica se ao juntar carrinho de user e anonimo não fica item duplicado
        no carrinho do user"""
        # seta um carrinho anonimo para a request com um item x
        # seta um user para a request
        # seta um carrinho para o user com o mesmo item x
        # manda um get para CartView
        # verifica se o item não duplicou e aumentou a quantidade
        pass


class RemoveFromCartTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def t_exclui_item_do_carrinho(self):
        """Verifica se ao mandar a request com a pk do produto do carrinho
        o item é excluido do carrinho"""
        # manda uma request get (a view esta configurada para dar post ao receber get) para RemoveFromCart
        # verifica se o item foi excluido do carrinho
        pass

    def t_tenta_excluir_item_que_nao_tem_no_carrinho(self):
        """Verifica se ao mandar uma request com a pk incorreta de um CartItem inexistente
        retorna um 404"""
        # manda uma request get para RemoveFromCart
        # verifica se é retornado um 404
        pass


class add_to_cartTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def t_adiciona_item_sem_ter_carrinho_anonimo(self):
        """Verifica se um user anonimo consegue adicionar item sem ter criado um carrinho ainda
        (deve ser criado um automaticamente)"""
        # com user anonimo e sem carrinho, manda uma request para add_to_cart com o pk do item à adicionar
        # verifica se foi criado um cart anonimo
        # verifica se foi adicionado o item para o cart anonimo
        pass

    def t_adiciona_item_ja_tendo_carrinho_anonimo(self):
        """Verifica se um user anonimo que já possui carrinho anonimo consegue adicionar
        itens no seu carrinho"""
        # com user anonimo e com carrinho, manda uma request para add_to_cart com o pk do item à adicionar
        # verifica se foi adicionado o item para o cart anonimo
        pass

    def t_adiciona_item_sem_ter_carrinho_user(self):
        """Verifica se um user logado que ainda não possui carrinho, consegue adicionar item
        e criar carrinho automaticamente"""
        # com um user logado e sem carrinho, manda uma request para add_to_cart com o pk do item à adicionar
        # verifica se foi criado um carrinho para o user
        # verifica se o item foi adicionado para o carrinho do user
        pass

    def t_adiciona_item_ja_tendo_carrinho_user(self):
        """Verifica se um user logado que já possui carrinho consegue adicionar item ao cart"""
        # com um user logado e com carrinho, manda uma request para add_to_cart com o pk do item à adicionar
        # verifica se foi adicionado no carrinho do user
        pass
