from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask.templating import TemplateNotFound
# from cadastro_usuario.rotas_cad_user import cad_user_bp
import os
import psycopg2

# os.chdir(r'D:\\Faculdade\\REPs\\Pyquiz')
print("Diretório atual:", os.getcwd())
app = Flask(__name__, template_folder='templates')

# app.register_blueprint(cad_user_bp, url_prefix='/usuario')  # Registra o blueprint com o prefixo /usuario

DB_HOST = "pyquiz.ctolbpze49xs.us-east-1.rds.amazonaws.com"  # Altere conforme necessário
DB_NAME = "pyquizt1"  # Nome do banco de dados
DB_USER = "postgres"  # Usuário do banco
DB_PASSWORD = "a11anl3tciaem4nue11"  # Senha do banco

@app.route("/")  
def home():
    return render_template("base.html")
@app.route("/user_login")  
def user_login():
    return render_template("user_login.html")

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
        print(data)
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
