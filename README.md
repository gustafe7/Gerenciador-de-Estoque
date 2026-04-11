# Gerenciador de Produtos — Django + PostgreSQL

## Stack
- Python 3.10+
- Django 4.2
- PostgreSQL
- HTML / CSS / JS (frontend mantido)

## Funcionalidades
- Autenticação de usuários (login/logout)
- Painel admin Django (`/admin`)
- CRUD de produtos via API JSON
- Proteção CSRF

## Estrutura
```
projeto_produtos_django/
├── core/               # Configurações do projeto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── produtos/           # App principal
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── static/
│   │   ├── style.css
│   │   └── script.js
│   └── templates/produtos/
│       ├── index.html
│       └── login.html
├── manage.py
├── requirements.txt
└── .env.example
```

## Como rodar

### 1. Instalar dependências
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente
```bash
cp .env.example .env
# Edite .env com suas credenciais do PostgreSQL
```

### 3. Criar banco de dados no PostgreSQL
```sql
CREATE DATABASE produtos_db;
```

### 4. Rodar migrações
```bash
python manage.py migrate
```

### 5. Criar superusuário (acesso ao admin e à aplicação)
```bash
python manage.py createsuperuser
```

### 6. Iniciar servidor
```bash
python manage.py runserver
```

Acesse em: http://localhost:8000  
Admin em: http://localhost:8000/admin

## Variáveis de ambiente (.env)
| Variável | Descrição |
|---|---|
| `SECRET_KEY` | Chave secreta Django |
| `DEBUG` | True em dev, False em prod |
| `DB_NAME` | Nome do banco PostgreSQL |
| `DB_USER` | Usuário PostgreSQL |
| `DB_PASSWORD` | Senha PostgreSQL |
| `DB_HOST` | Host do banco |
| `DB_PORT` | Porta (padrão 5432) |
