from django.test import TestCase, RequestFactory

from apps.user_app.models import UserModel
from apps.loja_app.models import ItensModel

class LojaModelsTest(TestCase):

    def setUp(self):
        self.request = RequestFactory()
        self.vendedor = UserModel.objects.create_superuser(
                email='supertest@gmail.com',
                username='superTest',
                password='123123123a',
                first_name= 'Super',
                last_name= 'Test',
                is_seller= True,
            )

    def test_cria_item(self):
        """Teste para se certificar que um item pode ser criado"""
        item = ItensModel.objects.create(
            nome = 'Teste Item 1',
            descricao =  'Este é o item de teste 1',
            valor = 123456,
            quantidade = 2,
            vendedor = self.vendedor,
            imagem = 'fotos/2021/07/30/scarlett.jpg'
        )
        self.assertEqual(item.nome, 'Teste Item 1')
        self.assertEqual(item.descricao, 'Este é o item de teste 1')
        self.assertEqual(item.valor, 123456)
        self.assertEqual(item.quantidade, 2)
        self.assertEqual(item.vendedor, self.vendedor)
        self.assertEqual(item.imagem, 'fotos/2021/07/30/scarlett.jpg')
