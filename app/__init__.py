from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'minha-chave-secreta'

from app import routes