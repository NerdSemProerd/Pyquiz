document.addEventListener('DOMContentLoaded', () => {
    // Elementos da UI
    const loginBtn = document.getElementById('btn-login');
    const usernameInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const errorMessage = console.log();

    // Evento de envio do formulário
    loginBtn.addEventListener('submit', async (event) => {
        event.preventDefault(); // Previne o envio padrão do formulário

        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();

        if (!username || !password) {
            errorMessage.textContent = 'Por favor, preencha todos os campos.';
            return;
        }

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            if (response.ok) {
                window.location.href = '/dashboard'; // Redireciona para o dashboard em caso de sucesso
            } else {
                const data = await response.json();
                errorMessage.textContent = data.error || 'Erro ao fazer login. Tente novamente.';
            }
        } catch (error) {
            console.error('Erro na requisição:', error);
            errorMessage.textContent = 'Erro ao conectar ao servidor. Tente novamente mais tarde.';
        }
    });
});
