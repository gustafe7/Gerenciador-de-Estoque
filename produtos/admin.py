from django.contrib import admin
from .models import Produto


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'preco', 'criado_em')
    search_fields = ('nome',)
    list_filter = ('criado_em',)
    ordering = ('-criado_em',)
