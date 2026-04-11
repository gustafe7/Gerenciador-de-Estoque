# Gerenciador de Estoque

Sistema web de gerenciamento de estoque com suporte a múltiplas empresas e equipes, desenvolvido com Django e PostgreSQL.

## Funcionalidades

- **Autenticação** — cadastro, login e logout de usuários
- **Empresas** — cada usuário pode criar ou participar de múltiplas empresas
- **Equipes** — administradores adicionam funcionários à empresa por username
- **Papéis** — Administrador (gerencia estoque + membros) e Funcionário (gerencia estoque)
- **Produtos** — criar, editar e excluir produtos com nome, preço, quantidade e categoria
- **Categorias** — organização de produtos por categoria, separada por empresa
- **Dashboard** — total de produtos, valor em estoque, produto mais caro e itens sem estoque
- **Busca e filtros** — busca por nome/categoria, filtro por categoria e ordenação
- **Paginação** — lista de produtos e histórico paginados
- **Histórico** — registro de todas as ações (criação, edição, exclusão) com filtros por ação e período
- **Exportar CSV** — exportação do estoque completo em planilha
- **Painel Admin** — interface administrativa do Django em `/admin`

## Tecnologias

- Python 3.14
- Django 5.2
- PostgreSQL
- HTML, CSS, JavaScript (sem frameworks front-end)

## Estrutura do projeto

```
gerenciador_estoque/
├── core/               # Configurações do projeto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── produtos/           # App principal
│   ├── migrations/
│   ├── static/
│   │   ├── script.js
│   │   └── style.css
│   ├── templates/produtos/
│   │   ├── login.html
│   │   ├── registro.html
│   │   ├── selecionar_empresa.html
│   │   ├── criar_empresa.html
│   │   └── index.html
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## Como rodar localmente

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/gerenciador-estoque.git
cd gerenciador-estoque
```

### 2. Criar ambiente virtual e instalar dependências
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente
```bash
copy .env.example .env
```
Edite o `.env` com suas credenciais do PostgreSQL.

### 4. Criar banco de dados no PostgreSQL
```sql
CREATE DATABASE produtos_db;
```

### 5. Rodar migrações
```bash
python manage.py migrate
```

### 6. Criar superusuário (acesso ao admin)
```bash
python manage.py createsuperuser
```

### 7. Iniciar servidor
```bash
python manage.py runserver
```

Acesse em: http://localhost:8000  
Admin em: http://localhost:8000/admin

## Variáveis de ambiente

| Variável | Descrição |
|---|---|
| `SECRET_KEY` | Chave secreta do Django |
| `DEBUG` | `True` em desenvolvimento, `False` em produção |
| `ALLOWED_HOSTS` | Hosts permitidos (separados por espaço) |
| `DB_NAME` | Nome do banco PostgreSQL |
| `DB_USER` | Usuário PostgreSQL |
| `DB_PASSWORD` | Senha PostgreSQL |
| `DB_HOST` | Host do banco (padrão: localhost) |
| `DB_PORT` | Porta do banco (padrão: 5432) |

## Como usar

1. Acesse `/registro/` e crie sua conta
2. Crie uma empresa ou entre em uma existente
3. Gerencie o estoque da empresa
4. Como administrador, adicione funcionários pelo username deles no painel **Equipe**
5. Exporte o estoque em CSV pelo botão na navbar
