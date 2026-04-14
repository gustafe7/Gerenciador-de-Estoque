from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

# Handler para página 404 personalizada
handler404 = 'produtos.views.custom_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('produtos.urls')),
]
