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

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('token', data.access_token);
                console.log("Aqui o token",  data.access_token)
                window.location.href = '/';
            } else {
                switch (response.status) {
                    case 404:
                        showError(`
                                    Email não encontrado! Não possui cadastro? 
                                    <a href="/form_cad_usuario" class="alert-link">
                                        Cadastre-se aqui
                                    </a>
                                `, true);
                        break;
                    case 401:
                        showError('Email ou senha incorretos.');
                        break;
                    case 500:
                        showError('Erro interno do servidor. Tente novamente mais tarde. Verifique os log do servidor');
                        break;
                    default:
                        showError('Erro desconhecido. Tente novamente.');
                }
            }
        } catch (error) {
            console.error('Erro na requisição:', error);
            showError('Erro ao conectar ao servidor. Tente novamente mais tarde.');
        }
    });

    function showError(message, isHTML = false) {
        if (isHTML) {
            errorMessage.innerHTML = message; // Permite HTML
        } else {
            errorMessage.textContent = message; // Apenas texto
        }
        errorMessage.classList.remove('d-none');
    }
});