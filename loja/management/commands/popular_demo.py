from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from loja.models import Produto
from decimal import Decimal
class Command(BaseCommand):
    help='Cria usuários e produtos para o laboratório'
    def handle(self,*args,**kwargs):
        admin,_=User.objects.get_or_create(username='professor',defaults={'is_staff':True,'is_superuser':True,'email':'professor@lab.local'})
        admin.set_password('Professor@123'); admin.is_staff=True; admin.is_superuser=True; admin.save()
        aluno,_=User.objects.get_or_create(username='aluno',defaults={'email':'aluno@lab.local'}); aluno.set_password('Aluno@123'); aluno.save()
        dados=[('Notebook','Notebook laboratório',Decimal('3500.00'),25),('Mouse','Mouse USB',Decimal('79.90'),100),('Teclado','Teclado ABNT2',Decimal('129.90'),80),('Monitor','Monitor 24',Decimal('899.00'),40),('SSD 1TB','SSD NVMe',Decimal('499.00'),50),('Headset','Headset USB',Decimal('249.90'),60)]
        for nome,desc,preco,estoque in dados: Produto.objects.get_or_create(nome=nome,defaults={'descricao':desc,'preco':preco,'estoque':estoque})
        self.stdout.write(self.style.SUCCESS('Demo criada. professor/Professor@123 e aluno/Aluno@123'))
