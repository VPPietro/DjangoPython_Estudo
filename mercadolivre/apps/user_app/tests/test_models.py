from django.test import TestCase

from apps.user_app.models import UserModel


class UserModelTest(TestCase):

    def setUp(self):
        pass

    def test_cria_um_usuario(self):
        # Cria um usuario padrão
        create_user = UserModel.objects.create_user(
            email = 'pietro@gmail.com',
            username = 'pietropv',
            password = '123456',
            first_name = 'pietro',
            last_name = 'vanelli')
        # Seleciona o user no db
        user = UserModel.objects.get(id=create_user.id)
        # Verifica se dados do usuário estão corretos
        self.assertEqual(user.email, 'pietro@gmail.com')
        self.assertEqual(user.username, 'pietropv')
        self.assertEqual(user.first_name, 'pietro')
        self.assertEqual(user.last_name, 'vanelli')
        # Verifica se valores padrões de superuser são Falsos
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.is_seller, False)

    def test_cria_um_superusuario(self):
        # Cria um superuser com o cria_superuser
        create_user = UserModel.objects.create_superuser(
            email = 'pietrosuper@gmail.com',
            username = 'pietropvsuper',
            password = '123456789',
            first_name = 'pietros',
            last_name = 'vanellis')
        # Seleciona o superuser na db
        superuser = UserModel.objects.get(id=create_user.id)
        # Verifica se os dados do superuser estão corretos
        self.assertEqual(superuser.email, 'pietrosuper@gmail.com')
        self.assertEqual(superuser.username, 'pietropvsuper')
        self.assertEqual(superuser.first_name, 'pietros')
        self.assertEqual(superuser.last_name, 'vanellis')
        # Verifica se os valores de superuser são Verdadeiros
        self.assertEqual(superuser.is_staff, True)
        self.assertEqual(superuser.is_superuser, True)
