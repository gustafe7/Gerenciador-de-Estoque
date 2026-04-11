import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Produto


# ── Auth ──────────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        error = 'Usuário ou senha inválidos.'

    return render(request, 'produtos/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')


# ── Página principal ───────────────────────────────────────────────────────────

@login_required
def index(request):
    return render(request, 'produtos/index.html')


# ── API JSON ───────────────────────────────────────────────────────────────────

@login_required
@require_http_methods(['GET'])
def listar_produtos(request):
    produtos = Produto.objects.all().values('id', 'nome', 'preco')
    data = [
        {'id': p['id'], 'nome': p['nome'], 'preco': float(p['preco'])}
        for p in produtos
    ]
    return JsonResponse(data, safe=False)


@login_required
@csrf_exempt
@require_http_methods(['POST'])
def criar_produto(request):
    try:
        data = json.loads(request.body)
        nome = data.get('nome', '').strip()
        preco = data.get('preco')

        if not nome or preco is None:
            return JsonResponse({'error': 'Dados incompletos'}, status=400)

        preco = float(preco)
        if preco < 0:
            return JsonResponse({'error': 'Preço inválido'}, status=400)

        produto = Produto.objects.create(nome=nome, preco=preco)
        return JsonResponse({'id': produto.id, 'nome': produto.nome, 'preco': float(produto.preco)}, status=201)

    except (ValueError, json.JSONDecodeError):
        return JsonResponse({'error': 'Dados inválidos'}, status=400)


@login_required
@csrf_exempt
@require_http_methods(['DELETE'])
def excluir_produto(request, id):
    try:
        produto = Produto.objects.get(pk=id)
        produto.delete()
        return JsonResponse({'sucesso': 'Produto excluído'})
    except Produto.DoesNotExist:
        return JsonResponse({'erro': 'Produto não encontrado'}, status=404)
