from django.urls import path
from . import views
urlpatterns=[
  path('',views.home,name='home'), path('produtos/',views.produtos,name='produtos'),
  path('login/',views.entrar,name='login'), path('logout/',views.sair,name='logout'),
  path('carrinho/',views.carrinho,name='carrinho'), path('carrinho/adicionar/<int:produto_id>/',views.adicionar_carrinho,name='adicionar_carrinho'),
  path('finalizar/',views.finalizar,name='finalizar'), path('pagamento/<int:pedido_id>/',views.pagamento,name='pagamento'),
  path('pagamento/<int:pedido_id>/confirmar/',views.pagamento_mock,name='pagamento_mock'),
  path('pedidos/',views.meus_pedidos,name='meus_pedidos'), path('painel/',views.painel,name='painel'),
  path('api/produtos/',views.api_produtos,name='api_produtos'), path('api/pedidos/<int:pedido_id>/',views.api_pedido,name='api_pedido'),
  path('health/',views.health,name='health'), path('lab/lento/',views.lab_lento,name='lab_lento'), path('lab/cpu/',views.lab_cpu,name='lab_cpu')]
