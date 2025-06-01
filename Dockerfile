# Usa uma imagem base com Python
FROM python:3.13

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos do projeto para o contêiner
COPY . /app

# Instala dependências do projeto
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Expõe a porta padrão do Flask
EXPOSE 5000

# Comando para iniciar o Flask
CMD ["python", "app.py"]
