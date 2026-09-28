from django.contrib import admin
from .models import Produto, Pedido, ItemPedido
admin.site.register([Produto,Pedido,ItemPedido])
