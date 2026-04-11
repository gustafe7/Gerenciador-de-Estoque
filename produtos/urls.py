from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Página
    path('', views.index, name='index'),

    # API
    path('produtos', views.listar_produtos, name='listar_produtos'),
    path('produtos/criar', views.criar_produto, name='criar_produto'),
    path('produtos/<int:id>', views.excluir_produto, name='excluir_produto'),
]
