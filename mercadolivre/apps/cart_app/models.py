from enum import auto
from django.db import models
from django.db.models.deletion import CASCADE

from apps.loja_app.models import ItensModel
from apps.user_app.models import UserModel


class CartItemModel(models.Model):
    loja_item = models.ForeignKey(ItensModel, on_delete=CASCADE)
    quantidade_compra = models.IntegerField(verbose_name='Quantidade do item no carrinho')
    time_item_added = models.TimeField(auto_now=True)

    class Meta:
        db_table = 'cart_item'

    # def __str__(self) -> str:
    #     return str(self.id)


class CartModel(models.Model):
    cart_item = models.ManyToManyField(CartItemModel)
    comprador = models.OneToOneField(UserModel, on_delete=CASCADE, null=True)
    time_cart_added = models.TimeField(auto_now=True)

    class Meta:
        db_table = 'cart_model'

    def __str__(self) -> str:
        return 'Cart id: ' + str(self.id)
