from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# Configurações SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USUARIO = "seuemail@gmail.com"
EMAIL_SENHA = "sua_senha_de_app"  # senha de app do Gmail

@app.route('/enviar-email', methods=['POST'])
def enviar_email():
    data = request.get_json()

    nome = data.get('nome')
    destinatario = data.get('email')

    if not nome or not destinatario:
        return jsonify({'error': 'nome e email são obrigatórios'}), 400

    # Monta o corpo do e-mail
    assunto = "Bem-vindo ao PyQuiz!"
    corpo = f"Olá {nome},\n\nObrigado por se registrar no PyQuiz!\n\nBoa sorte nos testes!"

    # Cria o objeto de mensagem
    mensagem = MIMEText(corpo)
    mensagem["Subject"] = assunto
    mensagem["From"] = EMAIL_USUARIO
    mensagem["To"] = destinatario

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as servidor:
            servidor.starttls()
            servidor.login(EMAIL_USUARIO, EMAIL_SENHA)
            servidor.send_message(mensagem)

        return jsonify({'status': 'ok', 'mensagem': f'E-mail enviado para {nome}'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
