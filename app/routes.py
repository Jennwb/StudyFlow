from app import app
from flask import render_template
from flask import request
from flask import flash, redirect
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='StudyFlow')

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		usuario = form.usuario.data
		senha = form.senha.data

		if usuario != 'admin' or senha != 'admin':
			if (usuario == 'admin'):
				flash('O login está correto.', "warning")
			else:
				flash('O login está incorreto. ', "danger")
			
			if (senha == 'admin'):
				flash('A senha está correta. ', "warning")
			else:
				flash('A senha está incorreta. ', "danger")
			return redirect("/login")
		else:
			return "{} - {}".format(form.usuario.data, form.senha.data)
	return render_template('login.html', form=form)

@app.route('/formregistrar')
def formregistrar():
	return render_template('registrar.html')

@app.route('/registrar', methods=['POST'])
def registrar():
	usuario = request.form.get("usuario")
	email = request.form.get("email")
	senha = request.form.get("senha")
	confsenha = request.form.get("confsenha")

	if senha == confsenha:
		return "As senhas são iguais!"
	else:
		return "As senhas são diferentes!"
	return "{} - {} - {} - {}".format(usuario, email, senha, confsenha)