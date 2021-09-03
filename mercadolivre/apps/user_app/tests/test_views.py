from django.test import TestCase, RequestFactory
from django.contrib.messages.storage.cookie import CookieStorage
from django.contrib.auth.models import AnonymousUser

from apps.user_app.models import UserModel
from apps.user_app.views import LoginClassView

def setup_std(self, factory=True, user=False, user2=False):
    self.factory = RequestFactory() if factory else None
    self.user = UserModel.objects.create_user(
        email='usertest@gmail.com',
        username='userTest',
        password='123123123a',
        first_name= 'User',
        last_name= 'Test',
        is_seller= False,) if user else None
    self.user2 = UserModel.objects.create_user(
        email='usertest2@gmail.com',
        username='userTest2',
        password='123123123a',
        first_name= 'User',
        last_name= 'Test',
        is_seller= False,) if user2 else None

class LoginViewTest(TestCase):

    def setUp(self):
        setup_std(self, user=True, user2=True)










    def test_login_com_usuario_incorreto(self):
        # manda uma request tipo post com informações de usuario incorretas
        data = {
            'username': 'usertest@gmail.com',
            'password': '123123123aerrado'}
        response = self.client.post('/user/login/', data, follow=True)
        # Verifica se a request continua com o user AnonymousUser()
        self.assertTrue(isinstance(response.context['user'], AnonymousUser))

















    def test_login_com_usuario_correto(self):
        # manda uma request tipo post com informações de usuario corretas
        # Verifica se a página foi redirecionada para 'lista-itens-user'
        # Verifica se a request esta com o user logado
        pass

    def test_acesso_a_pagina_login_com_usuario_ja_logado(self):
        # tenta mandar uma request do tipo get para a página de login
        self.request = self.factory.get('/user/login')
        self.request.user = self.user
        response = LoginClassView.as_view()(self.request)
        # Verifica se o usuario foi redirecionado para a pagina de 'lista-itens-user'
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], '/sua_loja/')
        # Verifica se a request continua com o user logado
        self.assertEqual(self.request.user, self.user)

    def test_tentativa_de_login_com_usuario_ja_logado(self):
        # manda uma request post para a página de login
        data={'username': 'usertest2@gmail.com', 'password': '123123123a'}
        self.request = self.factory.post('/user/login', data=data)
        self.request.user = self.user
        # Verifica se é retornado um código de erro (pois não possui csrftoken)
        response = LoginClassView.as_view()(self.request)
        self.assertEqual(response.status_code, 403)
        # Verifica se o usuário continua logado
        self.assertEqual(self.request.user, self.user)
