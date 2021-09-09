from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL

from apps.loja_app.models import ItensModel
from apps.user_app.models import UserModel


# class CartItemModel(models.Model):
#     item = models.OneToOneField(ItensModel, on_delete=CASCADE, default=7)
#     quantidade = models.IntegerField(verbose_name='Quantidade do item no carrinho')

#     class Meta:
#         db_table = 'cart_item'

#     def __str__(self) -> str:
#         return 'Item: ' + str(self.item_id)


class CartModel(models.Model):
    cart_item = models.OneToOneField(ItensModel, on_delete=SET_NULL, default=1, null=True)
    comprador = models.OneToOneField(UserModel, on_delete=CASCADE, null=True)

    class Meta:
        db_table = 'cart_model'

    def __str__(self) -> str:
        return 'CART comprador ' + str(self.comprador_id)
