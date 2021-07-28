from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from apps.loja_app.models import ItensModel
from apps.loja_app.views import ItemCreateView
from apps.user_app.models import UserModel


class LojaModelsTest(TestCase):

    def setUp(self):
        self.request = RequestFactory()

    def cria_item(self, nome: str, descricao: str, valor: float, quantidade: int, vendedor: UserModel, imagem: str) -> ItensModel:
        return ItensModel.objects.create(nome=nome, descricao=descricao, valor=valor, quantidade=quantidade, vendedor=vendedor, imagem=imagem)
    
    def criacao_item(self):
        i = self.cria_item('Teste de produto autoTest',
            'Teste criado automaticamente',
            1500,
            12,
            UserModel.objects.get(id=1),
            'img/no_foto_item.png')
        self.assertTrue(isinstance(i, ItensModel))
