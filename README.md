# Gerenciador de Estoque

Sistema web de gerenciamento de estoque com suporte a múltiplas empresas e equipes, desenvolvido com Django e PostgreSQL.

🔗 **Demo:** https://gerenciador-estoque-uuwt.onrender.com

---

## Sobre o projeto

Tenho formação técnica em Administração e, ao começar minha jornada no desenvolvimento web, quis unir as duas áreas em um projeto prático. O controle de estoque é uma necessidade real de qualquer negócio — e desenvolver uma solução completa para isso me permitiu aplicar tanto o conhecimento administrativo quanto as habilidades técnicas que venho adquirindo.

Com esse projeto aprendi a trabalhar com Django de forma mais aprofundada, a modelar bancos de dados relacionais com PostgreSQL, a estruturar uma API REST sem frameworks adicionais e a fazer o deploy de uma aplicação real em produção.

---

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
- **Página 404 personalizada** — experiência consistente em rotas inválidas
- **Favicon** — identidade visual na aba do navegador
- **Datas no horário local** — histórico exibido no fuso horário do usuário

## Tecnologias

- Python 3.14
- Django 5.2
- PostgreSQL
- WhiteNoise (arquivos estáticos em produção)
- Gunicorn (servidor WSGI em produção)
- HTML, CSS, JavaScript (sem frameworks front-end)

## Deploy

- **Aplicação:** Render
- **Banco de dados:** Railway (PostgreSQL)

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
│   │   ├── favicon.svg
│   │   ├── script.js
│   │   └── style.css
│   ├── templates/produtos/
│   │   ├── 404.html
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
├── build.sh
├── manage.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## Como rodar localmente

### 1. Clonar o repositório
```bash
git clone https://github.com/gustafe7/Gerenciador-de-Estoque.git
cd Gerenciador-de-Estoque
```

### 2. Criar ambiente virtual e instalar dependências
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente
```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
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
Admin em: http://localhost:8000/admin/

## Variáveis de ambiente

| Variável | Descrição |
|---|---|
| `SECRET_KEY` | Chave secreta do Django |
| `DEBUG` | `True` em desenvolvimento, `False` em produção |
| `ALLOWED_HOSTS` | Hosts permitidos (separados por espaço) |
| `CSRF_TRUSTED_ORIGINS` | Origem confiável para CSRF (URL do deploy) |
| `DB_NAME` | Nome do banco PostgreSQL |
| `DB_USER` | Usuário PostgreSQL |
| `DB_PASSWORD` | Senha PostgreSQL |
| `DB_HOST` | Host do banco (padrão: localhost) |
| `DB_PORT` | Porta do banco (padrão: 5432) |

## Recuperação de senha

O sistema não possui recuperação automática de senha por email. Caso um usuário esqueça a senha, o administrador pode redefini-la pelo painel admin:

1. Acesse `/admin/`
2. Vá em **Autenticação e Autorização → Usuários**
3. Clique no usuário desejado
4. Clique em **"Alterar senha"** no canto superior direito

## Como usar

1. Acesse `/registro/` e crie sua conta
2. Crie uma empresa ou entre em uma existente
3. Gerencie o estoque da empresa
4. Como administrador, adicione funcionários pelo username deles no painel **Equipe**
5. Exporte o estoque em CSV pelo botão na navbar
