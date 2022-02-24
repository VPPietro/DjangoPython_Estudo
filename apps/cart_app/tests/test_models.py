from django.test import TestCase


class CartModelTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def t_cria_cart_model(self):
        """Verifica se um cart model é criado corretamente com os padrões certos"""
        # cria um cart model
        # verifica dados
        pass

    def t_ao_deletar_cart_model_deleta_cart_items(self):
        """Verifica se ao deletar o CartModel o CASCADE deleta as informações
        do carrinho do db"""
        # cria um carrinho com cart items
        # deleta carrinho
        # verifica se tanto o carrinho quanto os cart items foi deletado
        pass


class CartItemTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def t_cria_um_cart_item_model(self):
        """Verifica se um cart item model é criado corretamente com os padrões certos"""
        # cria um cart item model
        # verifica dados
        pass
