from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask.templating import TemplateNotFound
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, TIMESTAMP,FLOAT
import json
# from cadastro_usuario.rotas_cad_user import cad_user_bp
import os
import psycopg2





# os.chdir(r'D:\\Faculdade\\REPs\\Pyquiz')
print("Diretório atual:", os.getcwd())
app = Flask(__name__, template_folder='templates')

# app.register_blueprint(cad_user_bp, url_prefix='/usuario')  # Registra o blueprint com o prefixo /usuario

DB_HOST = "192.168.1.3"  # Altere conforme necessário
DB_NAME = "pyquiz"  # Nome do banco de dados
DB_USER = "postgres"  # Usuário do banco
DB_PASSWORD = "a11anl3tciaem4nue11"  # Senha do banco




# Cadastro de banco com SQLAlchemy
# Configura o banco (pode ser SQLite, PostgreSQL, etc)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:a11anl3tciaem4nue11@192.168.1.3:5432/pyquiz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o SQLAlchemy com o app
db = SQLAlchemy(app)


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
    question_id = db.Column(db.Integer, db.ForeignKey('questao.id_questao'))






@app.route("/")  
def home():
    return render_template("base.html")
@app.route("/user_login")  
def user_login():
    return render_template("user_login.html")

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

        # print(request.form)
        

        print(f"Nome: {nome}")
        print(f"Sobrenome: {sobrenome}")
        print(f"Email: {email}")
        print(f"Telefone: {telefone}")
        print(f"Senha: {senha}")

        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            cur = conn.cursor()
            
            query = "INSERT INTO usuarios (nome, sobrenome, email, senha) VALUES (%s, %s, %s, %s)"
            cur.execute(query, (nome, sobrenome, email, senha))
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
        data = request.get_json()
       
        quiz_nome = data['name']
        print(quiz_nome)




        with open('quizpronto.json', 'w') as f:
            json.dump(data, f, indent=4)
    print("Data salva no quizpronto.json")
    return jsonify({'message': 'Quiz salvo com sucesso!'})

        # try:
        #     conn = psycopg2.connect(
        #         host=DB_HOST,
        #         database=DB_NAME,
        #         user=DB_USER,
        #         password=DB_PASSWORD
        #     )
        #     cur = conn.cursor()
            
        #     query = "INSERT INTO usuarios (nome, sobrenome, email, senha) VALUES (%s, %s, %s, %s)"
        #     cur.execute(query, (nome, sobrenome, email, senha))
        #     conn.commit()

        #     cur.close()
        #     conn.close()
        #     return "Cadastro realizado com sucesso!"
        # except Exception as e:
        #     return f"Erro ao cadastrar usuário: {e}"

if __name__ == "__main__":
    app.run(debug=True)
