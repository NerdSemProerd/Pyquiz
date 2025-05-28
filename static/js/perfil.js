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
    document.querySelector('.info-value.nome').textContent = dados.nome;
    document.querySelector('.info-value.email').textContent = dados.email;
    document.querySelector('.info-value.idade').textContent = dados.idade + ' anos';
    document.querySelector('.info-value.localizacao').textContent = dados.localizacao;
    document.querySelector('.info-value.biografia').textContent = dados.biografia;

    // Esconde "Carregando..." e mostra o conteúdo
    document.getElementById('carregando').style.display = 'none';
    document.getElementById('conteudo').style.display = 'block';
  } catch (erro) {
    console.error('Erro ao carregar perfil:', erro);
    document.getElementById('carregando').textContent = 'Erro ao carregar perfil.';
  }
}

carregarPerfil();

});
