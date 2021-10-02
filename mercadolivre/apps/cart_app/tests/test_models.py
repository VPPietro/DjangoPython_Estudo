from django.test import TestCase

from apps.cart_app.models import CartModel, CartItemModel
from apps.loja_app.models import ItensModel
from apps.user_app.models import UserModel


class CartModelTest(TestCase):

    def test_cria_cart_model(self):
        """Verifica se um cart model é criado corretamente com os padrões certos"""
        carrinho = CartModel.objects.create()
        self.assertTrue(isinstance(carrinho, CartModel))


class CartItemTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_cria_um_cart_item_model(self):
        """Verifica se um cart item model é criado corretamente com os padrões certos"""
        # cria um cart item model
        user = UserModel.objects.create(
            email = 'pietro@teste.com',
            username = 'PietroPV',
            first_name = 'pietro',
            last_name = 'paraventi',
            is_seller = True)
        item_loja = ItensModel.objects.create(
            nome = 'item loja',
            descricao = 'primeiro item da loja',
            valor = 100,
            quantidade = 10,
            vendedor = user)
        item_carrinho = CartItemModel.objects.create(
            loja_item = item_loja,
            quantidade_compra = 1)
        # verifica dados
        self.assertTrue(isinstance(item_carrinho, CartItemModel))
