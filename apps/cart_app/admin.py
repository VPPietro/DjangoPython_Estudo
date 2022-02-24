from django.contrib import admin

from apps.cart_app.models import CartModel, CartItemModel

admin.site.register(CartItemModel)
admin.site.register(CartModel)
