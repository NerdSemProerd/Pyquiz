document.addEventListener('DOMContentLoaded', function() {
    const quizzesContainer = document.getElementById('quizzes-container');
    
    // Função para carregar os quizzes
    function loadQuizzes() {
        // Mostra loading
        quizzesContainer.innerHTML = `
            <div class="col-12 text-center py-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Carregando...</span>
                </div>
            </div>
        `;
        
        // Faz a requisição
        fetch('/api/quizzes')
            .then(response => {
                if (!response.ok) throw new Error('Erro ao carregar quizzes');
                return response.json();
            })
            .then(quizzes => {
                // Limpa o container
                quizzesContainer.innerHTML = '';
                
                // Se não houver quizzes
                if (quizzes.length === 0) {
                    quizzesContainer.innerHTML = `
                        <div class="col-12 text-center py-5">
                            <h4 class="text-muted">Nenhum quiz disponível</h4>
                            <a href="/criar_quiz" class="btn btn-primary mt-3">
                                Criar Primeiro Quiz
                            </a>
                        </div>
                    `;
                    return;
                }
                
                // Cria os cards para cada quiz
                quizzes.forEach(quiz => {
                    const quizCard = `
                        <div class="col-md-6 col-lg-3 mb-4">
                            <div class="card h-100 quiz-card">
                                <div class="card-body d-flex flex-column">
                                    <h5 class="card-title">${quiz.nome}</h5>
                                    <p class="card-text text-muted flex-grow-1">
                                        ${quiz.descricao || 'Descrição não disponível'}
                                    </p>
                                    <a href="/quiz/${quiz.id}" class="btn btn-primary mt-auto">
                                        Fazer teste
                                    </a>
                                </div>
                            </div>
                        </div>
                    `;
                    quizzesContainer.insertAdjacentHTML('beforeend', quizCard);
                });
            })
            .catch(error => {
                console.error('Erro:', error);
                quizzesContainer.innerHTML = `
                    <div class="col-12 text-center py-5">
                        <h4 class="text-danger">Falha ao carregar quizzes</h4>
                        <p>${error.message}</p>
                        <button onclick="loadQuizzes()" class="btn btn-primary mt-3">
                            Tentar novamente
                        </button>
                    </div>
                `;
            });
    }
    
    // Carrega os quizzes quando a página abre
    loadQuizzes();
});