document.addEventListener('DOMContentLoaded', () => {
    // Elementos da UI
    const loginForm = document.getElementById('login-form');
    const usernameInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const errorMessage = document.getElementById('error-message'); // Corrigido aqui

    // Evento de envio do formulário
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        errorMessage.classList.add('d-none'); // Esconde mensagem de erro

        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();

        if (!username || !password) {
            showError('Por favor, preencha todos os campos.');
            return;
        }

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    email: username,  // Mudei para 'email' para bater com seu backend
                    password: password 
                })
            });

            if (response.ok) {
                window.location.href = '/dashboard';
            } else {
                const data = await response.json();
                showError(data.error || 'Erro ao fazer login. Tente novamente.');
            }
        } catch (error) {
            console.error('Erro na requisição:', error);
            showError('Erro ao conectar ao servidor. Tente novamente mais tarde.');
        }
    });

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.remove('d-none');
    }
});