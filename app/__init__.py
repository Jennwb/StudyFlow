from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'minha-chave-secreta'

#CONEXÃO COM O BANCO DE DADOS
usuario = "profaa16_codenow"
senha = "lQv4V1x27a"
servidor = "profaalbalopes.info"
banco = "profaa16_codenow"

#exemplo: mysql://username:password@server/db
conexao = "mysql://{0}:{1}@{2}/{3}".format(usuario, senha, servidor, banco)
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import routes