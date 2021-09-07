from django.db import models
from django.db.models.deletion import SET_NULL

from apps.loja_app.models import ItensModel
from apps.user_app.models import UserModel


class CartItemModel(models.Model):
    item = models.ManyToManyField(ItensModel)
    quantidade = models.IntegerField(verbose_name='Quantidade do item no carrinho', default=1)

    class Meta:
        db_table = 'cart_item'


class CartModel(models.Model):
    cart_item = models.ManyToManyField(CartItemModel)
    comprador = models.OneToOneField(UserModel, on_delete=SET_NULL, null=True)

    class Meta:
        db_table = 'cart_model'
