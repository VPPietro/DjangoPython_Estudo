from django.test import TestCase, RequestFactory

from apps.loja_app.models import ItensModel
from apps.user_app.models import UserModel


class LojaModelsTest(TestCase):

    def setUp(self):
        self.request = RequestFactory()

    def cria_item(self, nome: str, descricao: str, valor: float, quantidade: int, vendedor: UserModel, imagem: str) -> ItensModel:
        return ItensModel.objects.create(nome=nome, descricao=descricao, valor=valor, quantidade=quantidade, vendedor=vendedor, imagem=imagem)

    def criacao_item(self):
        i = self.cria_item('nome do produto',
            'descricao do produto',
            1500,
            12,
            UserModel.objects.get(id=1),
            'img/no_foto_item.png')
        self.assertTrue(isinstance(i, ItensModel))
        self.assertEqual(i.nome, 'nome do produto')
        self.assertEqual(i.descricao, 'descricao do produto')
        self.assertEqual(i.valor, 1500)
        self.assertEqual(i.quantidade, 12)
        self.assertEqual(i.imagem, 'img/no_foto_item.png')
