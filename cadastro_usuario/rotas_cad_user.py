# from flask import Blueprint, request
# from flask import jsonify, request
# import psycopg2

# cad_user_bp = Blueprint("cad_user", __name__)  # cria um blueprint chamado cad_user

# DB_HOST = "pyquiz.ctolbpze49xs.us-east-1.rds.amazonaws.com"  # Altere conforme necessário
# DB_NAME = "pyquizt1"  # Nome do banco de dados
# DB_USER = "postgres"  # Usuário do banco
# DB_PASSWORD = "a11anl3tciaem4nue11"  # Senha do banco


# @cad_user_bp.route("/cadastro_usuario", methods=['POST'])  
# def cad_usuario():
#     if request.method == 'POST':
        
#         # nome = request.form['nome']
#         nome = request.form.get("nome")
#         sobrenome = request.form.get("sobrenome")
#         email = request.form.get("email")
#         telefone = request.form.get("telefone")
#         senha = request.form.get("senha")

#         # print(request.form)
        

#         print(f"Nome: {nome}")
#         print(f"Sobrenome: {sobrenome}")
#         print(f"Email: {email}")
#         print(f"Telefone: {telefone}")
#         print(f"Senha: {senha}")

#         try:
#             conn = psycopg2.connect(
#                 host=DB_HOST,
#                 database=DB_NAME,
#                 user=DB_USER,
#                 password=DB_PASSWORD
#             )
#             cur = conn.cursor()
            
#             query = "INSERT INTO usuarios (nome, sobrenome, email, senha) VALUES (%s, %s, %s, %s)"
#             cur.execute(query, (nome, sobrenome, email, senha))
#             conn.commit()

#             cur.close()
#             conn.close()
#             return "Cadastro realizado com sucesso!"
#         except Exception as e:
#             return f"Erro ao cadastrar usuário: {e}"