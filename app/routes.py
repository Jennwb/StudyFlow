from app import app
from flask import render_template
from flask import request

@app.route('/')
@app.route('/index')
def index():
    nome = "Jennifer"
    return render_template('index.html', title='StudyFlow', nome=nome)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')
    return "{} e {}".format(usuario, senha)