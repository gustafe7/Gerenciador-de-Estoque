# Rotas do app produtos organizadas por domínio:
# - Auth: login, logout, registro
# - Empresa: seleção, criação e acesso
# - API REST: produtos, categorias, dashboard, histórico e membros
# - Exportação: CSV do estoque

from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),

    # Empresa
    path('empresas/', views.selecionar_empresa, name='selecionar_empresa'),
    path('empresas/criar/', views.criar_empresa, name='criar_empresa'),
    path('empresas/<int:empresa_id>/entrar/', views.entrar_empresa, name='entrar_empresa'),

    # Página principal
    path('', views.index, name='index'),

    # API Produtos
    path('api/produtos', views.listar_produtos, name='listar_produtos'),
    path('api/produtos/criar', views.criar_produto, name='criar_produto'),
    path('api/produtos/<int:id>/editar', views.editar_produto, name='editar_produto'),
    path('api/produtos/<int:id>/excluir', views.excluir_produto, name='excluir_produto'),

    # API Categorias
    path('api/categorias', views.listar_categorias, name='listar_categorias'),
    path('api/categorias/criar', views.criar_categoria, name='criar_categoria'),

    # API Dashboard e Histórico
    path('api/dashboard', views.dashboard, name='dashboard'),
    path('api/historico', views.listar_historico, name='listar_historico'),

    # Membros
    path('api/membros/adicionar', views.adicionar_membro, name='adicionar_membro'),
    path('api/membros/<int:membro_id>/remover', views.remover_membro, name='remover_membro'),

    # Exportar
    path('exportar/csv', views.exportar_csv, name='exportar_csv'),
]
