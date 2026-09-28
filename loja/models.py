from django.db import models
from django.contrib.auth.models import User
class Produto(models.Model):
    nome=models.CharField(max_length=120)
    descricao=models.TextField(blank=True)
    preco=models.DecimalField(max_digits=10,decimal_places=2)
    estoque=models.IntegerField(default=0)
    ativo=models.BooleanField(default=True)
    def __str__(self): return self.nome
class Pedido(models.Model):
    STATUS=[('ABERTO','Aberto'),('PAGO','Pago'),('CANCELADO','Cancelado')]
    usuario=models.ForeignKey(User,on_delete=models.CASCADE)
    criado_em=models.DateTimeField(auto_now_add=True)
    total=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    status=models.CharField(max_length=12,choices=STATUS,default='ABERTO')
class ItemPedido(models.Model):
    pedido=models.ForeignKey(Pedido,on_delete=models.CASCADE,related_name='itens')
    produto=models.ForeignKey(Produto,on_delete=models.PROTECT)
    quantidade=models.PositiveIntegerField(default=1)
    preco_unitario=models.DecimalField(max_digits=10,decimal_places=2)
