document.addEventListener('DOMContentLoaded', () => {
    // Elementos da UI
    const backButton = document.getElementById('back-button');
    const questionsContainer = document.getElementById('questions-container');
    const addQuestionBtn = document.getElementById('add-question-btn');
    const saveQuizBtn = document.getElementById('save-quiz-btn');
    let questions = []; // Array para controlar as questões

    // Voltar para a página anterior
    backButton.addEventListener('click', () => {
        window.history.back();
    });

    // Função para reordenar os números das questões
    function renumberQuestions() {
        const questionCards = document.querySelectorAll('.question-card');
        questions = Array.from(questionCards).map((card, index) => {
            const questionNumber = index + 1;
            card.setAttribute('data-id', questionNumber);
            card.id = `question-${questionNumber}`;
            card.querySelector('h3').textContent = `Questão ${questionNumber}`;
            return card;
        });
    }

    // Adicionar nova questão
    addQuestionBtn.addEventListener('click', () => {
        const questionNumber = questions.length + 1;
        const questionId = `question-${questionNumber}`;

        const questionHTML = `
        <div class="question-card" id="${questionId}" data-id="${questionNumber}">
            <div class="question-header">
                <h3>Questão ${questionNumber}</h3>
                <button type="button" class="btn btn-sm btn-danger delete-question">×</button>
            </div>
            <input type="text" class="form-control question-text" placeholder="Digite a pergunta..." required>
            <div class="answers-list mb-3"></div>
            <button type="button" class="btn btn-sm btn-outline-primary add-answer">
                + Adicionar Resposta
            </button>
        </div>`;

        questionsContainer.insertAdjacentHTML('beforeend', questionHTML);
        setupQuestionEvents(questionId);
        questions = [...questions, document.getElementById(questionId)];
    });

    // Configura o arrastar e soltar
    const sortable = new Sortable(questionsContainer, {
        animation: 150,
        handle: '.question-header',
        ghostClass: 'sortable-ghost',
        onEnd: function() {
            renumberQuestions();
        }
    });

    // Configura eventos para uma questão
    function setupQuestionEvents(questionId) {
        const questionEl = document.getElementById(questionId);
        
        // Adicionar resposta
        questionEl.querySelector('.add-answer').addEventListener('click', () => {
            const answersList = questionEl.querySelector('.answers-list');
            const answerCount = answersList.children.length + 1;
            
            const answerHTML = `
            <div class="answer-item row g-2 mb-2 align-items-center">
                <div class="col-md-7">
                    <input type="text" class="form-control answer-text" placeholder="Texto da resposta" required minlength="1">
                </div>
                <div class="col-md-3">
                    <input type="number" class="form-control answer-points" placeholder="Pontuação" step="0.1" min="0" required>
                </div>
                <div class="col-md-2">
                    <button type="button" class="btn btn-sm btn-outline-danger delete-answer">×</button>
                </div>
            </div>`;
            
            answersList.insertAdjacentHTML('beforeend', answerHTML);
        });

        // Delegation para deletar questão/resposta
        questionEl.addEventListener('click', (e) => {
            if (e.target.classList.contains('delete-question')) {
                if (confirm('Tem certeza que deseja excluir esta questão?')) {
                    questionEl.remove();
                    questions = questions.filter(q => q.id !== questionId);
                    renumberQuestions();
                }
            }
            
            if (e.target.classList.contains('delete-answer')) {
                e.target.closest('.answer-item').remove();
            }
        });
    }

    // Função para validar o quiz antes de salvar
    function validarQuiz() {
        let isValid = true;
        
        // Resetar estilos de erro
        document.querySelectorAll('.form-control').forEach(el => {
            el.classList.remove('is-invalid');
        });
        
        // Validar nome do quiz
        const quizName = document.getElementById('quiz-name');
        if (!quizName.value.trim()) {
            quizName.classList.add('is-invalid');
            isValid = false;
        }
        
        // Validar questões
        const questionCards = document.querySelectorAll('.question-card');
        if (questionCards.length === 0) {
            alert('Adicione pelo menos uma questão ao quiz!');
            return false;
        }
        
        questionCards.forEach((question, index) => {
            const questionText = question.querySelector('.question-text');
            const answers = question.querySelectorAll('.answer-item');
            
            // Validar texto da questão
            if (!questionText.value.trim()) {
                questionText.classList.add('is-invalid');
                isValid = false;
            }
            
            // Validar que há pelo menos uma resposta
            if (answers.length === 0) {
                alert(`A questão ${index + 1} precisa ter pelo menos uma resposta!`);
                isValid = false;
            }
            
            // Validar cada resposta
            answers.forEach(answer => {
                const answerText = answer.querySelector('.answer-text');
                const answerPoints = answer.querySelector('.answer-points');
                
                if (!answerText.value.trim()) {
                    answerText.classList.add('is-invalid');
                    isValid = false;
                }
                
                if (!answerPoints.value.trim() || isNaN(parseFloat(answerPoints.value))) {
                    answerPoints.classList.add('is-invalid');
                    isValid = false;
                }
            });
        });
        
        return isValid;
    }

    // Salvar quiz
    saveQuizBtn.addEventListener('click', () => {
        if (!validarQuiz()) {
            return; // Não continua se a validação falhar
        }
        
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
                    text: answer.querySelector('.answer-text').value,
                    points: parseFloat(answer.querySelector('.answer-points').value) || 0
                });
            });

            quizData.questions.push(questionData);
        });

        console.log('Dados do Quiz:', quizData);
        
        fetch('/salvar_quiz', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(quizData)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Quiz salvo com sucesso!', data);
            alert('Quiz salvo com sucesso!');
            window.location.href = '/';
        })
        .catch(error => {
            console.error('Erro ao salvar quiz:', error);
            alert('Erro ao salvar o quiz. Por favor, tente novamente.');
        });
    });
});