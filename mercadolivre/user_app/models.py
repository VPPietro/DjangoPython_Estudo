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
    date_joined = models.DateField(verbose_name='data de entrada', auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
      return self.username

    def get_is_superuser(self):
      return self.is_superuser

    def has_perm(self, app_label):  # Usado na página admin
      return self.is_superuser

    def has_module_perms(self, perm, obj=None):  # Usado na página admin
      return self.is_superuser
