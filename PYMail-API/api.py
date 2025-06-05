from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# Configurações do Gmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USUARIO = "juaresrossetto@gmail.com"  # Seu Gmail
EMAIL_SENHA = "hsku hudo qmfu myas "  # A senha de app que você gerou

@app.route('/enviar-email', methods=['POST'])
def enviar_email():
    data = request.get_json()
    
    nome = data.get('nome')
    destinatario = data.get('email')

    if not nome or not destinatario:
        return jsonify({'error': 'Nome e email são obrigatórios'}), 400

    assunto = "Login no PyQuiz detectado"
    corpo = f"Olá {nome},\n\nSeu login no PyQuiz foi registrado."

    mensagem = MIMEText(corpo)
    mensagem["Subject"] = assunto
    mensagem["From"] = EMAIL_USUARIO
    mensagem["To"] = destinatario

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USUARIO, EMAIL_SENHA)
            server.send_message(mensagem)
        return jsonify({'status': 'E-mail enviado!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=3000)