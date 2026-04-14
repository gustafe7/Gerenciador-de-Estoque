import json
import csv
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Sum, F, ExpressionWrapper, DecimalField
from django.core.paginator import Paginator

from .models import Produto, Categoria, HistoricoProduto, Empresa, MembroEmpresa


# ── Helpers ────────────────────────────────────────────────────────────────────

def get_empresa_ativa(request):
    """
    Retorna a empresa atualmente selecionada pelo usuário via sessão.
    Verifica se o usuário ainda é membro antes de retornar.
    Retorna None se nenhuma empresa estiver selecionada ou o acesso for inválido.
    """
    empresa_id = request.session.get('empresa_id')
    if not empresa_id:
        return None
    try:
        membro = MembroEmpresa.objects.select_related('empresa').get(
            empresa_id=empresa_id, usuario=request.user
        )
        return membro.empresa
    except MembroEmpresa.DoesNotExist:
        return None


def is_admin(request, empresa):
    """
    Verifica se o usuário logado é administrador da empresa informada.
    Usado para proteger ações restritas como adicionar/remover membros.
    """
    return MembroEmpresa.objects.filter(
        empresa=empresa, usuario=request.user, papel='admin'
    ).exists()


# ── Auth ───────────────────────────────────────────────────────────────────────

def login_view(request):
    """
    Exibe o formulário de login e autentica o usuário.
    Redireciona para seleção de empresa após login bem-sucedido.
    """
    if request.user.is_authenticated:
        return redirect('selecionar_empresa')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('selecionar_empresa')
        error = 'Usuário ou senha inválidos.'
    return render(request, 'produtos/login.html', {'error': error})


def registro_view(request):
    """
    Permite que novos usuários se cadastrem no sistema.
    Após o registro, o usuário é logado automaticamente e
    redirecionado para criar ou selecionar uma empresa.
    """
    if request.user.is_authenticated:
        return redirect('selecionar_empresa')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        if not username or not password1:
            error = 'Preencha todos os campos.'
        elif password1 != password2:
            error = 'As senhas não coincidem.'
        elif len(password1) < 6:
            error = 'A senha deve ter pelo menos 6 caracteres.'
        elif User.objects.filter(username=username).exists():
            error = 'Este usuário já existe.'
        else:
            user = User.objects.create_user(username=username, password=password1)
            login(request, user)
            return redirect('selecionar_empresa')
    return render(request, 'produtos/registro.html', {'error': error})


def logout_view(request):
    """
    Encerra a sessão do usuário e limpa todos os dados de sessão,
    incluindo a empresa ativa selecionada.
    """
    request.session.flush()
    logout(request)
    return redirect('login')


# ── Seleção de empresa ─────────────────────────────────────────────────────────

@login_required
def selecionar_empresa(request):
    """
    Lista todas as empresas das quais o usuário é membro.
    Ponto de entrada após o login — o usuário escolhe em qual empresa trabalhar.
    """
    empresas = MembroEmpresa.objects.select_related('empresa').filter(usuario=request.user)
    return render(request, 'produtos/selecionar_empresa.html', {'membros': empresas})


@login_required
def entrar_empresa(request, empresa_id):
    """
    Registra a empresa selecionada na sessão do usuário.
    Verifica se o usuário é membro antes de permitir o acesso.
    """
    get_object_or_404(MembroEmpresa, empresa_id=empresa_id, usuario=request.user)
    request.session['empresa_id'] = empresa_id
    return redirect('index')


@login_required
def criar_empresa(request):
    """
    Cria uma nova empresa e automaticamente adiciona o criador
    como administrador com papel 'admin'.
    """
    error = None
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        if not nome:
            error = 'Informe o nome da empresa.'
        else:
            empresa = Empresa.objects.create(nome=nome, dono=request.user)
            MembroEmpresa.objects.create(empresa=empresa, usuario=request.user, papel='admin')
            request.session['empresa_id'] = empresa.id
            return redirect('index')
    return render(request, 'produtos/criar_empresa.html', {'error': error})


# ── Página principal ───────────────────────────────────────────────────────────

@login_required
def index(request):
    """
    Página principal do sistema. Redireciona para seleção de empresa
    caso nenhuma esteja ativa na sessão.
    Passa os membros da equipe apenas para administradores.
    """
    empresa = get_empresa_ativa(request)
    if not empresa:
        return redirect('selecionar_empresa')
    admin = is_admin(request, empresa)
    membros = MembroEmpresa.objects.select_related('usuario').filter(empresa=empresa) if admin else []
    return render(request, 'produtos/index.html', {
        'empresa': empresa,
        'is_admin': admin,
        'membros': membros,
    })


# ── Gestão de membros ──────────────────────────────────────────────────────────

@login_required
@csrf_exempt
@require_http_methods(['POST'])
def adicionar_membro(request):
    """
    Adiciona um usuário existente à empresa como membro.
    Apenas administradores podem executar esta ação.
    O usuário precisa já ter uma conta no sistema para ser adicionado.
    """
    empresa = get_empresa_ativa(request)
    if not empresa or not is_admin(request, empresa):
        return JsonResponse({'error': 'Sem permissão'}, status=403)
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        papel = data.get('papel', 'funcionario')
        user = User.objects.get(username=username)
        if MembroEmpresa.objects.filter(empresa=empresa, usuario=user).exists():
            return JsonResponse({'error': 'Usuário já é membro'}, status=400)
        membro = MembroEmpresa.objects.create(empresa=empresa, usuario=user, papel=papel)
        return JsonResponse({'id': membro.id, 'username': user.username, 'papel': membro.papel})
    except User.DoesNotExist:
        return JsonResponse({'error': 'Usuário não encontrado'}, status=404)
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({'error': 'Dados inválidos'}, status=400)


@login_required
@csrf_exempt
@require_http_methods(['DELETE'])
def remover_membro(request, membro_id):
    """
    Remove um membro da empresa.
    O dono da empresa não pode ser removido.
    Apenas administradores podem executar esta ação.
    """
    empresa = get_empresa_ativa(request)
    if not empresa or not is_admin(request, empresa):
        return JsonResponse({'error': 'Sem permissão'}, status=403)
    try:
        membro = MembroEmpresa.objects.get(pk=membro_id, empresa=empresa)
        if membro.usuario == empresa.dono:
            return JsonResponse({'error': 'Não é possível remover o dono'}, status=400)
        membro.delete()
        return JsonResponse({'sucesso': 'Membro removido'})
    except MembroEmpresa.DoesNotExist:
        return JsonResponse({'error': 'Membro não encontrado'}, status=404)


# ── API Produtos ───────────────────────────────────────────────────────────────

@login_required
@require_http_methods(['GET'])
def listar_produtos(request):
    """
    Retorna os produtos da empresa ativa com suporte a:
    - Busca por nome ou categoria (parâmetro 'q')
    - Filtro por categoria (parâmetro 'categoria')
    - Ordenação por campo (parâmetro 'ordem')
    - Paginação com 10 itens por página
    """
    empresa = get_empresa_ativa(request)
    if not empresa:
        return JsonResponse({'error': 'Nenhuma empresa selecionada'}, status=400)

    qs = Produto.objects.select_related('categoria').filter(empresa=empresa)

    busca = request.GET.get('q', '').strip()
    if busca:
        qs = qs.filter(Q(nome__icontains=busca) | Q(categoria__nome__icontains=busca))

    categoria_id = request.GET.get('categoria')
    if categoria_id:
        qs = qs.filter(categoria_id=categoria_id)

    # Valida o campo de ordenação para evitar injeção de parâmetros inválidos
    ordem = request.GET.get('ordem', '-criado_em')
    if ordem in ['nome', '-nome', 'preco', '-preco', 'quantidade', '-quantidade', 'criado_em', '-criado_em']:
        qs = qs.order_by(ordem)

    page = int(request.GET.get('page', 1))
    paginator = Paginator(qs, 10)
    pagina = paginator.get_page(page)

    return JsonResponse({
        'produtos': [
            {
                'id': p.id, 'nome': p.nome, 'preco': float(p.preco),
                'quantidade': p.quantidade,
                'categoria': p.categoria.nome if p.categoria else None,
                'categoria_id': p.categoria_id,
                'criado_em': p.criado_em.strftime('%d/%m/%Y'),
            }
            for p in pagina
        ],
        'total': paginator.count,
        'paginas': paginator.num_pages,
        'pagina_atual': page,
    })


@login_required
@require_http_methods(['GET'])
def dashboard(request):
    """
    Retorna os indicadores do estoque da empresa ativa:
    - Total de produtos cadastrados
    - Valor total em estoque (preço × quantidade)
    - Produto mais caro
    - Quantidade de produtos com estoque zerado
    """
    empresa = get_empresa_ativa(request)
    if not empresa:
        return JsonResponse({'error': 'Nenhuma empresa selecionada'}, status=400)

    qs = Produto.objects.filter(empresa=empresa)
    total_produtos = qs.count()

    # Calcula o valor total multiplicando preço pela quantidade de cada produto
    valor_total = float(
        qs.aggregate(
            v=Sum(ExpressionWrapper(F('preco') * F('quantidade'), output_field=DecimalField()))
        ).get('v') or 0
    )
    mais_caro = qs.order_by('-preco').values('nome', 'preco').first()
    sem_estoque = qs.filter(quantidade=0).count()

    return JsonResponse({
        'total_produtos': total_produtos,
        'valor_total_estoque': valor_total,
        'mais_caro': mais_caro and {'nome': mais_caro['nome'], 'preco': float(mais_caro['preco'])},
        'sem_estoque': sem_estoque,
    })


@login_required
@csrf_exempt
@require_http_methods(['POST'])
def criar_produto(request):
    """
    Cria um novo produto vinculado à empresa ativa.
    Registra a ação no histórico com preço e quantidade iniciais.
    A categoria é opcional — se informada, deve pertencer à mesma empresa.
    """
    empresa = get_empresa_ativa(request)
    if not empresa:
        return JsonResponse({'error': 'Nenhuma empresa selecionada'}, status=400)
    try:
        data = json.loads(request.body)
        nome = data.get('nome', '').strip()
        preco = data.get('preco')
        quantidade = int(data.get('quantidade', 0))
        categoria_id = data.get('categoria_id')

        if not nome or preco is None:
            return JsonResponse({'error': 'Dados incompletos'}, status=400)

        preco = float(preco)
        if preco < 0:
            return JsonResponse({'error': 'Preço inválido'}, status=400)

        categoria = None
        if categoria_id:
            try:
                categoria = Categoria.objects.get(pk=categoria_id, empresa=empresa)
            except Categoria.DoesNotExist:
                pass

        produto = Produto.objects.create(
            empresa=empresa, nome=nome, preco=preco,
            quantidade=quantidade, categoria=categoria
        )
        HistoricoProduto.objects.create(
            empresa=empresa, produto_nome=produto.nome, acao='criado', usuario=request.user,
            detalhes=f'Preço: R$ {produto.preco} | Qtd: {produto.quantidade}'
        )
        return JsonResponse({
            'id': produto.id, 'nome': produto.nome, 'preco': float(produto.preco),
            'quantidade': produto.quantidade,
            'categoria': produto.categoria.nome if produto.categoria else None,
            'categoria_id': produto.categoria_id,
            'criado_em': produto.criado_em.strftime('%d/%m/%Y'),
        }, status=201)
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({'error': 'Dados inválidos'}, status=400)


@login_required
@csrf_exempt
@require_http_methods(['PUT'])
def editar_produto(request, id):
    """
    Atualiza os dados de um produto da empresa ativa.
    Registra no histórico o nome anterior e os novos valores.
    Garante que o produto pertence à empresa antes de editar.
    """
    empresa = get_empresa_ativa(request)
    if not empresa:
        return JsonResponse({'error': 'Nenhuma empresa selecionada'}, status=400)
    try:
        produto = Produto.objects.get(pk=id, empresa=empresa)
    except Produto.DoesNotExist:
        return JsonResponse({'erro': 'Produto não encontrado'}, status=404)
    try:
        data = json.loads(request.body)
        nome_antes = produto.nome
        produto.nome = data.get('nome', produto.nome).strip()
        produto.preco = float(data.get('preco', produto.preco))
        produto.quantidade = int(data.get('quantidade', produto.quantidade))
        categoria_id = data.get('categoria_id')
        produto.categoria = Categoria.objects.get(pk=categoria_id, empresa=empresa) if categoria_id else None
        produto.save()
        HistoricoProduto.objects.create(
            empresa=empresa, produto_nome=produto.nome, acao='editado', usuario=request.user,
            detalhes=f'Nome anterior: {nome_antes} | Preço: R$ {produto.preco} | Qtd: {produto.quantidade}'
        )
        return JsonResponse({
            'id': produto.id, 'nome': produto.nome, 'preco': float(produto.preco),
            'quantidade': produto.quantidade,
            'categoria': produto.categoria.nome if produto.categoria else None,
            'categoria_id': produto.categoria_id,
            'criado_em': produto.criado_em.strftime('%d/%m/%Y'),
        })
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({'error': 'Dados inválidos'}, status=400)


@login_required
@csrf_exempt
@require_http_methods(['DELETE'])
def excluir_produto(request, id):
    """
    Remove um produto da empresa ativa e registra a exclusão no histórico.
    Garante que o produto pertence à empresa antes de deletar.
    """
    empresa = get_empresa_ativa(request)
    if not empresa:
        return JsonResponse({'error': 'Nenhuma empresa selecionada'}, status=400)
    try:
        produto = Produto.objects.get(pk=id, empresa=empresa)
        nome = produto.nome
        produto.delete()
        HistoricoProduto.objects.create(empresa=empresa, produto_nome=nome, acao='excluido', usuario=request.user)
        return JsonResponse({'sucesso': 'Produto excluído'})
    except Produto.DoesNotExist:
        return JsonResponse({'erro': 'Produto não encontrado'}, status=404)


# ── API Categorias ─────────────────────────────────────────────────────────────

@login_required
@require_http_methods(['GET'])
def listar_categorias(request):
    """Retorna todas as categorias da empresa ativa."""
    empresa = get_empresa_ativa(request)
    if not empresa:
        return JsonResponse([], safe=False)
    cats = Categoria.objects.filter(empresa=empresa).values('id', 'nome')
    return JsonResponse(list(cats), safe=False)


@login_required
@csrf_exempt
@require_http_methods(['POST'])
def criar_categoria(request):
    """
    Cria uma nova categoria para a empresa ativa.
    Usa get_or_create para evitar duplicatas dentro da mesma empresa.
    """
    empresa = get_empresa_ativa(request)
    if not empresa:
        return JsonResponse({'error': 'Nenhuma empresa selecionada'}, status=400)
    try:
        data = json.loads(request.body)
        nome = data.get('nome', '').strip()
        if not nome:
            return JsonResponse({'error': 'Nome obrigatório'}, status=400)
        cat, created = Categoria.objects.get_or_create(nome=nome, empresa=empresa)
        return JsonResponse({'id': cat.id, 'nome': cat.nome}, status=201 if created else 200)
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({'error': 'Dados inválidos'}, status=400)


# ── API Histórico ──────────────────────────────────────────────────────────────

@login_required
@require_http_methods(['GET'])
def listar_historico(request):
    """
    Retorna o histórico de ações da empresa ativa com suporte a:
    - Filtro por tipo de ação (criado, editado, excluido)
    - Filtro por período (hoje, 7 dias, 30 dias)
    - Paginação com 10 itens por página
    """
    from datetime import date, timedelta
    empresa = get_empresa_ativa(request)
    if not empresa:
        return JsonResponse({'historico': [], 'total': 0, 'paginas': 1, 'pagina_atual': 1})

    page = int(request.GET.get('page', 1))
    acao = request.GET.get('acao', '')
    periodo = request.GET.get('periodo', '')

    qs = HistoricoProduto.objects.select_related('usuario').filter(empresa=empresa)

    if acao:
        qs = qs.filter(acao=acao)
    if periodo == 'hoje':
        qs = qs.filter(data__date=date.today())
    elif periodo == '7dias':
        qs = qs.filter(data__date__gte=date.today() - timedelta(days=7))
    elif periodo == '30dias':
        qs = qs.filter(data__date__gte=date.today() - timedelta(days=30))

    paginator = Paginator(qs, 10)
    pagina = paginator.get_page(page)
    return JsonResponse({
        'historico': [
            {
                'produto': h.produto_nome, 'acao': h.acao,
                'usuario': h.usuario.username if h.usuario else 'Sistema',
                'detalhes': h.detalhes,
                'data': h.data.isoformat(),
            }
            for h in pagina
        ],
        'total': paginator.count,
        'paginas': paginator.num_pages,
        'pagina_atual': page,
    })


# ── Exportar CSV ───────────────────────────────────────────────────────────────

@login_required
def exportar_csv(request):
    """
    Gera e retorna um arquivo CSV com todos os produtos da empresa ativa.
    O BOM (\\ufeff) é adicionado para garantir compatibilidade com Excel.
    O nome do arquivo inclui o nome da empresa para identificação.
    """
    empresa = get_empresa_ativa(request)
    if not empresa:
        return redirect('selecionar_empresa')
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="estoque_{empresa.nome}.csv"'
    response.write('\ufeff')
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nome', 'Categoria', 'Preço', 'Quantidade', 'Valor em Estoque', 'Cadastrado em'])
    for p in Produto.objects.select_related('categoria').filter(empresa=empresa):
        writer.writerow([
            p.id, p.nome,
            p.categoria.nome if p.categoria else '-',
            f'{float(p.preco):.2f}', p.quantidade,
            f'{float(p.preco) * p.quantidade:.2f}',
            p.criado_em.strftime('%d/%m/%Y'),
        ])
    return response


# ── Página de erro 404 ─────────────────────────────────────────────────────────

def custom_404(request, exception=None):
    """Página 404 personalizada exibida quando uma rota não é encontrada."""
    return render(request, 'produtos/404.html', status=404)
