document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const quizId = urlParams.get('quiz_id') || document.getElementById('quizId').value;
  
  fetch(`/api/quiz/${quizId}`)
      .then(response => response.json())
      .then(data => iniciarQuiz(data))
      .catch(error => console.error('Erro ao carregar quiz:', error));
});

function iniciarQuiz(quizData) {
  const perguntas = quizData.perguntas.map(pergunta => ({
      pergunta: pergunta.pergunta,
      opcoes: pergunta.opcoes.map(opcao => opcao.texto),
      resposta: pergunta.resposta
  }));

  let perguntaAtual = 0;
  let pontuacao = 0;
  let respostaSelecionada = null;

  const perguntaContainer = document.getElementById("perguntaContainer");
  const opcoesContainer = document.getElementById("opcoesContainer");
  const proximaBtn = document.getElementById("proximaBtn");
  const resultadoFinal = document.getElementById("resultadoFinal");

  function carregarPergunta() {
      const perguntaObj = perguntas[perguntaAtual];
      perguntaContainer.innerHTML = `<h2>${perguntaObj.pergunta}</h2>`;
      opcoesContainer.innerHTML = "";
      proximaBtn.disabled = true;
      respostaSelecionada = null;

      perguntaObj.opcoes.forEach(opcao => {
          const btn = document.createElement("button");
          btn.innerText = opcao;
          btn.classList.add("opcao");
          btn.onclick = () => selecionarResposta(btn, opcao);
          opcoesContainer.appendChild(btn);
      });
  }

  function selecionarResposta(botao, resposta) {
      document.querySelectorAll(".opcao").forEach(btn => btn.classList.remove("selecionada"));
      botao.classList.add("selecionada");
      respostaSelecionada = resposta;
      proximaBtn.disabled = false;
  }

  proximaBtn.onclick = () => {
      if (respostaSelecionada === perguntas[perguntaAtual].resposta) {
          pontuacao++;
      }

      perguntaAtual++;

      if (perguntaAtual < perguntas.length) {
          carregarPergunta();
      } else {
          mostrarResultado();
      }
  };

  function mostrarResultado() {
      document.getElementById("quizContainer").style.display = "none";
      resultadoFinal.style.display = "block";
      resultadoFinal.innerHTML = `
          <h2>Quiz Finalizado!</h2>
          <p>Sua pontuação: ${pontuacao} de ${perguntas.length}</p>
          <p>Quiz: ${quizData.nome}</p>
      `;
  }

  carregarPergunta();
}