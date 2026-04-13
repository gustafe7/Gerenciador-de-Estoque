# Configuração do painel administrativo do Django.
# Permite gerenciar todos os dados do sistema via /admin.
# Apenas superusuários têm acesso a este painel.

from django.contrib import admin
from .models import Produto, Categoria, HistoricoProduto, Empresa, MembroEmpresa


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'dono', 'criado_em')
    search_fields = ('nome',)


@admin.register(MembroEmpresa)
class MembroAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'empresa', 'papel', 'adicionado_em')
    list_filter = ('papel',)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'empresa')
    search_fields = ('nome',)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'empresa', 'categoria', 'preco', 'quantidade', 'criado_em')
    search_fields = ('nome',)
    list_filter = ('empresa', 'categoria', 'criado_em')


@admin.register(HistoricoProduto)
class HistoricoAdmin(admin.ModelAdmin):
    # Histórico é somente leitura — não deve ser editado manualmente
    list_display = ('produto_nome', 'acao', 'usuario', 'empresa', 'data')
    list_filter = ('acao', 'empresa')
    readonly_fields = ('produto_nome', 'acao', 'usuario', 'empresa', 'detalhes', 'data')
