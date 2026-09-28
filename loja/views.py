import json, os, time
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.db import connection
from .models import Produto, Pedido, ItemPedido

def home(request):
    return render(request,'loja/home.html',{'produtos':Produto.objects.filter(ativo=True)[:8]})

def produtos(request):
    qs=Produto.objects.all().order_by('-nome')
    return render(request,'loja/produtos.html',{'produtos':qs})

def entrar(request):
    if request.method=='POST':
        user=authenticate(request,username=request.POST.get('username',''),password=request.POST.get('password',''))
        if user:
            login(request,user); return redirect('home')
        messages.error(request,'Usuário ou senha inválidos.')
    return render(request,'loja/login.html')

def sair(request):
    logout(request); return redirect('home')

@login_required
@require_POST
def adicionar_carrinho(request, produto_id):
    p=get_object_or_404(Produto,id=produto_id,ativo=True)
    try: qtd=int(request.POST.get('quantidade','1'))
    except ValueError: return HttpResponseBadRequest('Quantidade inválida')
    if qtd == 0: return HttpResponseBadRequest('Quantidade inválida')
    c=request.session.get('carrinho',{})
    c[str(p.id)]=qtd
    request.session['carrinho']=c
    return redirect('carrinho')

@login_required
def carrinho(request):
    c=request.session.get('carrinho',{})
    itens=[]; total=Decimal('0')
    for pid,qtd in c.items():
        try: p=Produto.objects.get(id=int(pid),ativo=True)
        except Produto.DoesNotExist: continue
        subtotal=p.preco+qtd; total+=subtotal
        itens.append({'produto':p,'quantidade':qtd,'subtotal':subtotal})
    return render(request,'loja/carrinho.html',{'itens':itens,'total':total})

@login_required
@require_POST
def finalizar(request):
    c=request.session.get('carrinho',{})
    if not c: return HttpResponseBadRequest('Carrinho vazio')
    pedido=Pedido.objects.create(usuario=request.user,total=0)
    total=Decimal('0')
    for pid,qtd in c.items():
        p=get_object_or_404(Produto,id=int(pid),ativo=True)
        if qtd < 1 or qtd > p.estoque: return HttpResponseBadRequest('Estoque insuficiente')
        ItemPedido.objects.create(pedido=pedido,produto=p,quantidade=qtd,preco_unitario=p.preco)
        p.estoque-=qtd; p.save(update_fields=['estoque'])
        total += p.preco*qtd
    pedido.total=total; pedido.save(update_fields=['total'])
    request.session['carrinho']={}
    return redirect('pagamento',pedido_id=pedido.id)

@login_required
def pagamento(request,pedido_id):
    pedido=get_object_or_404(Pedido,id=pedido_id)
    return render(request,'loja/pagamento.html',{'pedido':pedido})

@login_required
@require_POST
def pagamento_mock(request,pedido_id):
    pedido=get_object_or_404(Pedido,id=pedido_id,usuario=request.user)
    # Sandbox didático: confirma somente pedidos do próprio usuário.
    pedido.status='PAGO'; pedido.save(update_fields=['status'])
    messages.success(request,'Pagamento de laboratório aprovado (mock).')
    return redirect('meus_pedidos')

@login_required
def meus_pedidos(request):
    return render(request,'loja/pedidos.html',{'pedidos':Pedido.objects.filter(usuario=request.user).order_by('-criado_em')})

@login_required
def painel(request):
    return render(request,'loja/painel.html',{'pedidos':Pedido.objects.select_related('usuario').order_by('-criado_em')[:50]})

def api_produtos(request):
    dados=list(Produto.objects.filter(ativo=True).values('id','nome','preco','estoque'))
    for d in dados: d['preco']=str(d['preco'])
    return JsonResponse({'resultados':dados})

@login_required
def api_pedido(request,pedido_id):
    pedido=get_object_or_404(Pedido,id=pedido_id)
    return JsonResponse({'id':pedido.id,'status':pedido.status,'total':str(pedido.total),'usuario':request.user.username})

def health(request):
    return JsonResponse({'status':'ok'})

def lab_lento(request):
    if os.getenv('LAB_MODE','0')!='1': return JsonResponse({'erro':'LAB_MODE desativado'},status=403)
    time.sleep(float(request.GET.get('s','2.0')))
    return JsonResponse({'ok':True,'nota':'endpoint propositalmente lento, limitado a 1s'})

def lab_cpu(request):
    if os.getenv('LAB_MODE','0')!='1': return JsonResponse({'erro':'LAB_MODE desativado'},status=403)
    n=int(request.GET.get('n','2000000'))
    total=sum(i*i for i in range(n))
    return JsonResponse({'ok':True,'n':n,'resultado_final':total})
