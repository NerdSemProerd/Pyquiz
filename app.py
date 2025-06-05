from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask.templating import TemplateNotFound
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import requests
# from cadastro_usuario.rotas_cad_user import cad_user_bp
import os




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

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Univel123*marcos@pyquiz.cyb5mu8yf2kt.us-east-1.rds.amazonaws.com:5432/pyquiz'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:a11anl3tciaem4nue11@192.168.192.45:5432/pyquiz'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:a11anl3tciaem4nue11@192.168.1.3:5432/pyquiz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o SQLAlchemy com o app
db = SQLAlchemy(app)


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    idade = db.Column(db.Integer)
    localizacao = db.Column(db.String(100))
    senha_hash = db.Column(db.String(255), nullable=False)
    autonomia = db.Column(db.String(20), default='user')  # 'user' ou 'admin'

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
    # pontuacao = db.Column(db.Float)
    correta = db.Column(db.Boolean, default=False)
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
    try:
        j_data = request.get_json()
        if not j_data:
            return jsonify({'message': 'Dados de login não fornecidos'}), 400
            
        j_email = j_data.get('email')
        j_password = j_data.get('password')

        if not j_email or not j_password:
            return jsonify({'message': 'Email e senha são obrigatórios'}), 400

        cred_usuario = Usuario.query.filter_by(email=j_email).first()
        
        # Verificação de credenciais
        if not cred_usuario or not check_password_hash(cred_usuario.senha_hash, j_password):
            return jsonify({'message': 'Email ou senha incorretos!'}), 401
        
        # Login bem-sucedido
        session['usuario_id'] = cred_usuario.id_usuario
        
        # Preparar dados para o email
        nome_completo = f"{cred_usuario.nome} {cred_usuario.sobrenome}"
        email = cred_usuario.email
        
        # Chamar a API de email local (opcional)
        try:
            resposta = requests.post(
                "http://localhost:3000/enviar-email",
                json={
                    "nome": nome_completo,
                    "email": email
                },
                timeout=3  # timeout de 3 segundos
            )
            
            if resposta.status_code != 200:
                print(f"AVISO: Email não enviado - {resposta.text}")
        
        except Exception as e:
            print(f"AVISO: Serviço de email indisponível - {str(e)}")
        
        return jsonify({
            'mensagem': 'Login realizado com sucesso',
            'usuario': {
                'id': cred_usuario.id_usuario,
                'nome': cred_usuario.nome,
                'email': cred_usuario.email
            }
        })

    except Exception as e:
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500



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
        data = request.get_json()
        
        # Verifica se o email já existe
        if Usuario.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email já cadastrado'}), 400
            
        try:
            novo_usuario = Usuario(
                nome=data['nome'],
                sobrenome=data['sobrenome'],
                email=data['email'],
                telefone=data.get('telefone'),
                idade=data.get('idade'),
                localizacao=data.get('localizacao'),
                senha_hash=generate_password_hash(data['senha'])
            )
            
            db.session.add(novo_usuario)
            db.session.commit()
            
            return jsonify({'message': 'Cadastro realizado com sucesso!'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
        

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
                correta=resposta_json['correta'],
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
                    'correta': resposta.correta
                }
                questao_data['opcoes'].append(opcao)
                
                # Verifica se é a resposta correta
                if resposta.correta:
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
