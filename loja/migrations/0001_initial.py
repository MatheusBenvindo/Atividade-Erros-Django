from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="Produto",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=120)),
                ("descricao", models.TextField(blank=True)),
                ("preco", models.DecimalField(decimal_places=2, max_digits=10)),
                ("estoque", models.IntegerField(default=0)),
                ("ativo", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Pedido",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                ("total", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("status", models.CharField(choices=[("ABERTO", "Aberto"), ("PAGO", "Pago"), ("CANCELADO", "Cancelado")], default="ABERTO", max_length=12)),
                ("usuario", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="ItemPedido",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantidade", models.PositiveIntegerField(default=1)),
                ("preco_unitario", models.DecimalField(decimal_places=2, max_digits=10)),
                ("pedido", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="itens", to="loja.pedido")),
                ("produto", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="loja.produto")),
            ],
        ),
    ]
