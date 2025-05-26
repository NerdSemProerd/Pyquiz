from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask.templating import TemplateNotFound
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, TIMESTAMP,FLOAT
from werkzeug.security import generate_password_hash
import json
# from cadastro_usuario.rotas_cad_user import cad_user_bp
import os
import psycopg2





# os.chdir(r'D:\\Faculdade\\REPs\\Pyquiz')
print("Diretório atual:", os.getcwd())
app = Flask(__name__, template_folder='templates')

# app.register_blueprint(cad_user_bp, url_prefix='/usuario')  # Registra o blueprint com o prefixo /usuario

# DB_HOST = "192.168.192.45"  # Altere conforme necessário
DB_HOST = "192.168.1.3"  
DB_NAME = "pyquiz"  # Nome do banco de dados
DB_USER = "postgres"  # Usuário do banco
DB_PASSWORD = "a11anl3tciaem4nue11"  # Senha do banco


# Cadastro de banco com SQLAlchemy
# Configura o banco (pode ser SQLite, PostgreSQL, etc)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:a11anl3tciaem4nue11@192.168.192.45:5432/pyquiz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:a11anl3tciaem4nue11@192.168.1.3:5432/pyquiz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o SQLAlchemy com o app
db = SQLAlchemy(app)


class Usuario(db.Model):
    _tablename_ = 'usuarios'

    id_nome = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(255))
    senha_hash = db.Column(db.String(128))
    autonomia = db.Column(db.String(20), default='user')  # 'Comum' ou 'Admin'

class Quiz_nome(db.Model):
    __tablename__ = 'quiz'

    id_quiz = db.Column(db.Integer, primary_key=True)
    nome_quiz = db.Column(db.String(255))
    descricao_quiz = db.Column(db.Text)
    
    questoes = db.relationship('Quiz_questao', backref='quiz', cascade="all, delete")


class Quiz_questao(db.Model):
    __tablename__ = 'questao'

    id_questao = db.Column(db.Integer, primary_key=True)
    questao = db.Column(db.String(255))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id_quiz'))

    respostas = db.relationship('Questao_resposta', backref='questao', cascade="all, delete")


class Questao_resposta(db.Model):
    __tablename__ = 'questao_resposta'

    id_resposta = db.Column(db.Integer, primary_key=True)
    resposta = db.Column(db.String(255))
    pontuacao = db.Column(db.Float)
    question_id = db.Column('id_questao', db.Integer, db.ForeignKey('questao.id_questao'))  # Mapeia para a coluna correta




@app.route("/")  
def home():
    return render_template("base.html")




@app.route("/user_login")  
def user_login():
    return render_template("user_login.html")





@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        json_data_login = request.get_json()
        obter_credenciais(json_data_login)
    return jsonify({'message': 'Credenciais recebidas com sucesso!'})
def obter_credenciais(json_data_login):
    email_login=json_data_login['username'],
    senha_login=json_data_login['password']

    print(f"Email: {email_login}")
    print(f"Senha: {senha_login}")
    return ...




@app.route("/form_cad_usuario")  
def form_cad_usuario():
    return render_template("cadastro_user.html")

# Teste de conexão com o banco de dados

# @app.route("/testar_conexao")
# def testar_conexao():
#     try:
#         db.session.execute(text("SELECT 1"))
#         return "Conexão com o banco bem-sucedida!"
#     except Exception as e:
#         return f"Erro ao conectar: {e}"

        
@app.route("/cadastro_usuario", methods=['POST'])  
def cad_usuario():
    if request.method == 'POST':
        
        # nome = request.form['nome']
        nome = request.form.get("nome")
        sobrenome = request.form.get("sobrenome")
        email = request.form.get("email")
        telefone = request.form.get("telefone")
        senha = request.form.get("senha")

        senha_hash = generate_password_hash(senha)
        
        # print(request.form)
        print(f"Nome: {nome}")
        print(f"Sobrenome: {sobrenome}")
        print(f"Email: {email}")
        print(f"Telefone: {telefone}")
        print(f"Senha: {senha_hash}")

        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            cur = conn.cursor()
            
            query = "INSERT INTO usuarios (nome, sobrenome, email, senha_hash) VALUES (%s, %s, %s, %s)"
            cur.execute(query, (nome, sobrenome, email, senha_hash))
            conn.commit()

            cur.close()
            conn.close()
            return "Cadastro realizado com sucesso!"
        except Exception as e:
            return f"Erro ao cadastrar usuário: {e}"
        
        
@app.route('/criar_quiz')
def criar_quiz():
    return render_template("quiz_maker.html")



@app.route("/salvar_quiz", methods=['POST'])  
def cad_quiz():
    if request.method == 'POST':
        json_data = request.get_json()
        salvar_quiz(json_data)
    return jsonify({'message': 'Quiz salvo com sucesso!'})
def salvar_quiz(json_data):
    # 1. Cria o quiz
    novo_quiz = Quiz_nome(
        nome_quiz=json_data['name'],
        descricao_quiz=json_data['description']
    )
    db.session.add(novo_quiz)
    db.session.flush()  # garante que o ID do quiz será gerado

    # 2. Cria as questões e respostas
    for questao_json in json_data['questions']:
        nova_questao = Quiz_questao(
            questao=questao_json['text'],  # Alterado para 'text' que é a chave no JSON
            quiz_id=novo_quiz.id_quiz
        )
        db.session.add(nova_questao)
        db.session.flush()  # garante que o ID da questão será gerado

        # 3. Respostas da questão
        for resposta_json in questao_json['answers']:
            nova_resposta = Questao_resposta(
                resposta=resposta_json['text'],  # Alterado para 'text' que é a chave no JSON
                pontuacao=resposta_json['points'],
                question_id=nova_questao.id_questao
            )
            db.session.add(nova_resposta)
    db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
