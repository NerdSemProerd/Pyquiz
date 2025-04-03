document.addEventListener('DOMContentLoaded', function() {
    const questionsContainer = document.getElementById('questionsContainer');
    const addQuestionBtn = document.getElementById('addQuestion');
    
    // Contador para IDs únicos
    let questionCount = 0;
    
    // Adiciona nova questão
    addQuestionBtn.addEventListener('click', function() {
        questionCount++;
        const questionId = `question-${questionCount}`;
        
        const questionHTML = `
        <div class="card mb-4 question-card" id="${questionId}" data-id="${questionCount}">
            <div class="card-header bg-light d-flex justify-content-between align-items-center">
                <span>Questão #${questionCount}</span>
                <button type="button" class="btn btn-sm btn-danger delete-question">×</button>
            </div>
            <div class="card-body">
                <div class="form-group">
                    <label>Enunciado:</label>
                    <input type="text" class="form-control" name="questions[${questionCount}][text]" required>
                </div>
                
                <div class="answers-container mb-3" data-question-id="${questionCount}">
                    <!-- Respostas serão adicionadas aqui -->
                </div>
                
                <button type="button" class="btn btn-sm btn-outline-primary add-answer">
                    + Adicionar Resposta
                </button>
                
                <div class="form-group mt-3">
                    <label>Pontuação Total:</label>
                    <input type="number" class="form-control total-score" name="questions[${questionCount}][total_score]" min="1" value="1">
                </div>
            </div>
        </div>`;
        
        questionsContainer.insertAdjacentHTML('beforeend', questionHTML);
        initQuestionEvents(questionId);
    });
    
    // Inicializa arrastar/soltar
    new Sortable(questionsContainer, {
        animation: 150,
        handle: '.card-header',
    });
});

function initQuestionEvents(questionId) {
    const questionElement = document.getElementById(questionId);
    
    // Adicionar resposta
    questionElement.querySelector('.add-answer').addEventListener('click', function() {
        const questionDataId = questionElement.getAttribute('data-id');
        const answersContainer = questionElement.querySelector('.answers-container');
        const answerCount = answersContainer.children.length + 1;
        
        const answerHTML = `
        <div class="answer-item mb-2 d-flex align-items-center">
            <div class="flex-grow-1 mr-2">
                <input type="text" class="form-control" name="questions[${questionDataId}][answers][${answerCount}][text]" placeholder="Texto da resposta" required>
            </div>
            <div class="ml-2" style="width: 100px;">
                <input type="number" class="form-control" name="questions[${questionDataId}][answers][${answerCount}][score]" placeholder="Pontos" min="0" step="0.1">
            </div>
            <button type="button" class="btn btn-sm btn-outline-danger ml-2 delete-answer">×</button>
        </div>`;
        
        answersContainer.insertAdjacentHTML('beforeend', answerHTML);
    });
    
    // Delegation para deletar questão/resposta
    questionElement.addEventListener('click', function(e) {
        if (e.target.classList.contains('delete-question')) {
            e.target.closest('.question-card').remove();
        }
        
        if (e.target.classList.contains('delete-answer')) {
            e.target.closest('.answer-item').remove();
        }
    });
}