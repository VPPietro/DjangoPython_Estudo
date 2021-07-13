from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):

  def __create_user(self, email, password, is_staff, is_superuser, **extra_fields):
    if not email:
        raise ValueError('digita o email')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        email=email,
        is_staff=is_staff,
        is_active=True,
        is_superuser=is_superuser,
        last_login=now,
        date_joined=now,
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password, **extra_fields):
    return self.__create_user(email, password, False, False, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    return self.__create_user(email, password, True, True, **extra_fields)


class UserModel(AbstractBaseUser):

    email =  models.EmailField(max_length=255, verbose_name='email', unique=True)
    username = models.CharField(max_length=255, verbose_name='nickname', unique=True)
    first_name = models.CharField(max_length=255, verbose_name='Primeiro nome')
    last_name = models.CharField(max_length=255, verbose_name='Sobrenome')
    date_joined = models.DateField(verbose_name='data de entrada', auto_now_add=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
      return self.username

    def has_perms(self, app_label):  # Usado na página admin and the decorator os class based view
      return self.is_superuser

    def has_module_perms(self, perm, obj=None):  # Usado na página admin
      return self.is_superuser

    def get_is_superuser(self):
      return self.is_superuser

    def get_full_name(self):
      return self.first_name + ' ' +  self.last_name

    def get_first_name(self):
      return self.first_name

    def set_first_name(self, new_first_name):
      self.first_name = new_first_name
      self.save()

    def get_last_name(self):
      return self.last_name

    def set_last_name(self, new_last_name):
      self.last_name = new_last_name
      self.save()

    def get_email(self):
      return self.email

    def set_email(self, new_email):
      self.email = new_email
      self.save()

    def get_data_cadastro(self):
      return self.date_joined

    def get_id(self):
      return self.id
