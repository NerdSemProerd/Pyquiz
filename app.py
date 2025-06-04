from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask.templating import TemplateNotFound
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

# from cadastro_usuario.rotas_cad_user import cad_user_bp
import os
import psycopg2




# os.chdir(r'D:\\Faculdade\\REPs\\Pyquiz')
print("Diretório atual:", os.getcwd())
app = Flask(__name__, template_folder='templates')
app = Flask(__name__)
app.secret_key = 'chave-muito-secreta'
# app.register_blueprint(cad_user_bp, url_prefix='/usuario')  # Registra o blueprint com o prefixo /usuario

# DB_HOST = "192.168.192.45"  # Altere conforme necessário
# DB_HOST = "192.168.1.3"  
DB_HOST = "pyquiz.cyb5mu8yf2kt.us-east-1.rds.amazonaws.com"
DB_NAME = "pyquiz"  # Nome do banco de dados
DB_USER = "postgres"  # Usuário do banco
DB_PASSWORD = "Univel123*marcos"  # Senha do banco



app.config['SECRET_KEY'] = 'super_senha_secreta123'  # Substitua pela sua chave secreta
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Define o tempo de expiração do token JWT

# Cadastro de banco com SQLAlchemy
# Configura o banco (pode ser SQLite, PostgreSQL, etc)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://Univel123*marcos@pyquiz.cyb5mu8yf2kt.us-east-1.rds.amazonaws.com'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:a11anl3tciaem4nue11@192.168.192.45:5432/pyquiz'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:a11anl3tciaem4nue11@192.168.1.3:5432/pyquiz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o SQLAlchemy com o app
db = SQLAlchemy(app)


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(255))
    senha_hash = db.Column(db.String(255))
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
    usuario = None
    if 'usuario_id' in session:
        usuario = db.session.get(Usuario, session['usuario_id'])
    return render_template("base.html", usuario=usuario)



@app.route("/user_login")  
def user_login():
    return render_template("user_login.html")


@app.route("/login", methods=['POST'])
def login():
    j_data = request.get_json()
    j_email = j_data.get('email')
    j_password = j_data.get('password')

    cred_usuario = Usuario.query.filter_by(email=j_email).first()
    if not cred_usuario:
        return jsonify({'message': 'Email não encontrado'}), 404
    else:
        if not cred_usuario or not check_password_hash(cred_usuario.senha_hash, j_password):
            return jsonify({'message': 'Email ou senha incorretos!'}), 401
    if cred_usuario and check_password_hash(cred_usuario.senha_hash, j_password):
            
        session['usuario_id'] = cred_usuario.id_usuario
        return jsonify({'mensagem': 'Login realizado com sucesso'})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route("/form_cad_usuario")  
def form_cad_usuario():
    return render_template("cadastro_user.html")

        
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
            return "Cadastro realizado com sucesso!" and redirect('/')
        except Exception as e:
            return f"Erro ao cadastrar usuário: {e}"
        

@app.route('/perfil')
def perfil():
    if 'usuario_id' not in session:
        return redirect('/user_login')  # não logado
    if 'usuario_id' in session:
        usuario = db.session.get(Usuario, session['usuario_id'])
    
    return render_template("perfil.html", usuario=usuario)


@app.route('/carregar/perfil')
def carregar_perfil():
    try:
        usuario_id = session.get('usuario_id')
        
        if not usuario_id:
            return jsonify({'message': 'Usuário não encontrado'}), 404
        usuario = db.session.get(Usuario, session['usuario_id'])
        # Retorna os dados do usuário
        return jsonify({
            'id': usuario.id_usuario,
            'nome': usuario.nome,
            'email': usuario.email,
            'autonomia': usuario.autonomia
        })
    except Exception as e:
        return jsonify({'message': str(e)}), 500

    


@app.route('/criar_quiz')
def criar_quiz():
    if 'usuario_id' not in session:
        return redirect('/user_login')  # não logado
    if 'usuario_id' in session:
        usuario = db.session.get(Usuario, session['usuario_id'])
    return render_template("quiz_maker.html", usuario=usuario)



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


@app.route('/api/quizzes')
def get_quizzes():
    try:
        # Busca apenas nome e descrição dos quizzes
        quizzes = Quiz_nome.query.with_entities(
            Quiz_nome.id_quiz,
            Quiz_nome.nome_quiz,
            Quiz_nome.descricao_quiz
        ).all()
        
        # Formata os dados para JSON
        quizzes_data = [{
            'id': quiz.id_quiz,
            'nome': quiz.nome_quiz,
            'descricao': quiz.descricao_quiz
        } for quiz in quizzes]
        
        return jsonify(quizzes_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# @app.route("/responda")  
# def responda():
#     if 'usuario_id' not in session:
#         return redirect('/user_login')  # não logado
#     if 'usuario_id' in session:
#         usuario = db.session.get(Usuario, session['usuario_id'])
#     return render_template("responda.html", usuario=usuario)

@app.route('/api/quiz/<int:quiz_id>')
def get_quiz_questions(quiz_id):
    try:
        # Busca o quiz e suas questões com respostas
        quiz = Quiz_nome.query.get_or_404(quiz_id)
        
        # Formata os dados para JSON
        quiz_data = {
            'id': quiz.id_quiz,
            'nome': quiz.nome_quiz,
            'descricao': quiz.descricao_quiz,
            'perguntas': []
        }
        
        for questao in quiz.questoes:
            questao_data = {
                'id': questao.id_questao,
                'pergunta': questao.questao,
                'opcoes': [],
                'resposta': None
            }
            
            for resposta in questao.respostas:
                opcao = {
                    'texto': resposta.resposta,
                    'pontuacao': resposta.pontuacao
                }
                questao_data['opcoes'].append(opcao)
                
                # Assumindo que a resposta correta é a com maior pontuação
                if resposta.pontuacao == 1.0:  # ou qualquer lógica que determine a resposta correta
                    questao_data['resposta'] = resposta.resposta
            
            quiz_data['perguntas'].append(questao_data)
        
        return jsonify(quiz_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route("/responda/<int:quiz_id>")  
def responda(quiz_id):
    if 'usuario_id' not in session:
        return redirect('/user_login')  # não logado
    
    usuario = db.session.get(Usuario, session['usuario_id'])
    return render_template("responda.html", usuario=usuario, quiz_id=quiz_id)



if __name__ == "__main__":
    app.run(debug=True)
