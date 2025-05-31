function showTab(tabId, event) {
    const tabs = document.querySelectorAll('.tab-content');
    const buttons = document.querySelectorAll('.tab-btn');

    tabs.forEach(tab => tab.classList.remove('active'));
    buttons.forEach(btn => btn.classList.remove('active'));

    document.getElementById(tabId).classList.add('active');
    event.target.classList.add('active');
}

document.addEventListener('DOMContentLoaded', () => {
async function carregarPerfil() {
  try {
    const resposta = await fetch('/carregar/perfil'); // ou qualquer endpoint que você criou no Flask
    const dados = await resposta.json();

    // Aqui você preenche os campos com os dados recebidos
    document.getElementById('user-name').textContent = dados.nome;
    document.getElementById('user-email').textContent = dados.email;
    document.getElementById('user-age').textContent = dados.idade + ' anos';
    document.getElementById('user-location').textContent = dados.localizacao;
    document.getElementById('user-bio').textContent = dados.biografia;

  } catch (erro) {
    console.error('Erro ao carregar perfil:', erro);
  }
}

carregarPerfil();

});
