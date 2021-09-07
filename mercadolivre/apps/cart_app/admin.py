from django.contrib import admin

from apps.cart_app.models import CartItemModel, CartModel

admin.site.register(CartItemModel)
admin.site.register(CartModel)
