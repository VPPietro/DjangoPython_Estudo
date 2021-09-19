from enum import auto
from django.db import models
from django.db.models.deletion import CASCADE
from datetime import date, datetime

from apps.loja_app.models import ItensModel
from apps.user_app.models import UserModel


class CartItemModel(models.Model):
    loja_item = models.ForeignKey(ItensModel, on_delete=CASCADE)
    quantidade_compra = models.IntegerField(verbose_name='Quantidade do item no carrinho')
    time_item_added = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart_item'

    # def __str__(self) -> str:
    #     return str(self.id)


class CartModel(models.Model):
    cart_item = models.ManyToManyField(CartItemModel, through='CartLink')
    comprador = models.OneToOneField(UserModel, on_delete=CASCADE, null=True)
    time_cart_added = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart_model'

    # def __str__(self) -> str:
    #     return 'Cart id: ' + str(self.id)


class CartLink(models.Model):
    """Por padrão a tabela que o django cria automaticamente para ManyToMany vem com 'on_delete=RESTRICT',
    então foi definido a tabela manualmente com CASCADE"""
    cartmodel_id = models.ForeignKey(CartModel, on_delete=CASCADE)
    cartitem_id = models.ForeignKey(CartItemModel, on_delete=CASCADE)

    class Meta:
        db_table = 'cart_model_has_cart_item'
