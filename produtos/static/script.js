const form = document.getElementById('form-produto');
const lista = document.getElementById('lista-produtos');
const contador = document.getElementById('contador');

function getCsrfToken() {
    return document.cookie
        .split(';')
        .map(c => c.trim())
        .find(c => c.startsWith('csrftoken='))
        ?.split('=')[1] || '';
}

function atualizarContador(n) {
    if (contador) contador.textContent = n;
}

function emptyState() {
    return `<li class="empty" id="empty-msg" style="list-style:none;text-align:center;padding:2.5rem 1rem;color:#aaa;font-size:14px;background:none;box-shadow:none;">Nenhum produto cadastrado ainda.</li>`;
}

async function carregarProdutos() {
    const resposta = await fetch('/produtos');
    const produtos = await resposta.json();

    lista.innerHTML = produtos.length === 0 ? emptyState() : '';

    produtos.forEach(produto => {
        const li = document.createElement('li');
        li.setAttribute('data-id', produto.id);
        li.innerHTML = `
            <div class="produto-icon">📦</div>
            <div class="produto-info">
                <div class="produto-nome">${produto.nome}</div>
                <div class="produto-preco">R$ ${produto.preco.toFixed(2)}</div>
            </div>
            <button class="btn-excluir excluir">Excluir</button>
        `;
        lista.appendChild(li);
    });

    atualizarContador(produtos.length);
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const nome = document.getElementById('nome').value;
    const preco = parseFloat(document.getElementById('preco').value);

    const resposta = await fetch('/produtos/criar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify({ nome, preco })
    });

    if (resposta.ok) {
        document.getElementById('nome').value = '';
        document.getElementById('preco').value = '';
        carregarProdutos();
    } else {
        alert('Erro ao adicionar produto');
    }
});

lista.addEventListener('click', async (e) => {
    if (e.target.classList.contains('excluir')) {
        const li = e.target.closest('li');
        const id = li.getAttribute('data-id');

        const resposta = await fetch(`/produtos/${id}`, {
            method: 'DELETE',
            headers: { 'X-CSRFToken': getCsrfToken() },
        });

        if (resposta.ok) {
            li.remove();
            const total = lista.querySelectorAll('li[data-id]').length;
            atualizarContador(total);
            if (total === 0) lista.innerHTML = emptyState();
        } else {
            alert('Erro ao excluir produto');
        }
    }
});

window.onload = carregarProdutos;

