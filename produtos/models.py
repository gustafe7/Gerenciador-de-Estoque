from django.db import models
from django.contrib.auth.models import User


class Empresa(models.Model):
    nome = models.CharField(max_length=150)
    dono = models.ForeignKey(User, on_delete=models.CASCADE, related_name='empresas_criadas')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['-criado_em']

    def __str__(self):
        return self.nome


class MembroEmpresa(models.Model):
    PAPEIS = [
        ('admin', 'Administrador'),
        ('funcionario', 'Funcionário'),
    ]
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='membros')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='membros')
    papel = models.CharField(max_length=20, choices=PAPEIS, default='funcionario')
    adicionado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('empresa', 'usuario')
        verbose_name = 'Membro'
        verbose_name_plural = 'Membros'

    def __str__(self):
        return f'{self.usuario.username} — {self.empresa.nome} ({self.papel})'


class Categoria(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='categorias')
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']
        unique_together = ('empresa', 'nome')

    def __str__(self):
        return self.nome


class Produto(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='produtos')
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='produtos')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return f'{self.nome} - R$ {self.preco}'


class HistoricoProduto(models.Model):
    ACOES = [
        ('criado', 'Criado'),
        ('editado', 'Editado'),
        ('excluido', 'Excluído'),
    ]
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='historico', null=True)
    produto_nome = models.CharField(max_length=100)
    acao = models.CharField(max_length=10, choices=ACOES)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    detalhes = models.TextField(blank=True)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data']
        verbose_name = 'Histórico'
        verbose_name_plural = 'Histórico'

    def __str__(self):
        return f'{self.acao} - {self.produto_nome}'
