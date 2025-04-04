document.addEventListener('DOMContentLoaded', () => {
    // Elementos da UI
    const backButton = document.getElementById('back-button');
    const questionsContainer = document.getElementById('questions-container');
    const addQuestionBtn = document.getElementById('add-question-btn');
    const saveQuizBtn = document.getElementById('save-quiz-btn');
    let questionCount = 0;

    // Voltar para a página anterior
    backButton.addEventListener('click', () => {
        window.history.back();
    });

    // Adicionar nova questão
    addQuestionBtn.addEventListener('click', () => {
        questionCount++;
        const questionId = `question-${questionCount}`;

        const questionHTML = `
        <div class="question-card" id="${questionId}" data-id="${questionCount}">
            <div class="question-header">
                <h3>Questão ${questionCount}</h3>
                <button class="btn btn-danger delete-btn delete-question">×</button>
            </div>
            <input type="text" class="question-text" placeholder="Digite a pergunta..." required>
            <div class="answers-list"></div>
            <button type="button" class="btn btn-outline-secondary add-answer-btn add-answer">
                + Adicionar Resposta
            </button>
        </div>`;

        questionsContainer.insertAdjacentHTML('beforeend', questionHTML);
        setupQuestionEvents(questionId);
    });

    // Configura o arrastar e soltar
    new Sortable(questionsContainer, {
        animation: 150,
        handle: '.question-header',
        ghostClass: 'sortable-ghost'
    });

    // Salvar quiz
    saveQuizBtn.addEventListener('click', () => {
        const quizData = {
            name: document.getElementById('quiz-name').value,
            description: document.getElementById('quiz-description').value,
            questions: []
        };

        document.querySelectorAll('.question-card').forEach(question => {
            const questionData = {
                text: question.querySelector('.question-text').value,
                answers: []
            };

            question.querySelectorAll('.answer-item').forEach(answer => {
                questionData.answers.push({
                    text: answer.querySelector('input[type="text"]').value,
                    points: parseFloat(answer.querySelector('input[type="number"]').value) || 0
                });
            });

            quizData.questions.push(questionData);
        });

        console.log('Dados do Quiz:', quizData);
        // Aqui você faria a requisição para o Flask
    });

    // Configura eventos para uma questão
    function setupQuestionEvents(questionId) {
        const question = document.getElementById(questionId);
        
        question.querySelector('.add-answer').addEventListener('click', () => {
            const answersList = question.querySelector('.answers-list');
            const answerHTML = `
            <div class="answer-item">
                <input type="text" placeholder="Resposta" required>
                <input type="number" placeholder="Pontos" min="0" step="0.1">
                <button class="btn btn-sm btn-danger delete-btn delete-answer">×</button>
            </div>`;
            answersList.insertAdjacentHTML('beforeend', answerHTML);
        });

        question.addEventListener('click', (e) => {
            if (e.target.classList.contains('delete-question')) {
                question.remove();
            }
            if (e.target.classList.contains('delete-answer')) {
                e.target.closest('.answer-item').remove();
            }
        });
    }

    // Simulação do usuário logado (remova quando implementar)
    document.getElementById('username').textContent = 'Nome do Usuário';
    document.getElementById('profile-pic').textContent = 'NU';
});