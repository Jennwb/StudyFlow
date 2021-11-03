from app import app
from flask import render_template
from flask import request
from flask import flash, redirect
from app.forms import LoginForm, RegistrarForm
from app.models.usuario import Usuario
from app import db
import bcrypt
from app import conexao

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
		ativo = 1
		salt = bcrypt.gensalt(8)
		senha_hashed = bcrypt.hashpw(form.senha.data.encode('utf8'), salt)

	# Autenticação
		if usuario == 'admin' and senha == 'admin':
			return "{} - {}".format(form.usuario.data, form.senha.data)
		else:
			usuario_db = Usuario.query.filter_by(nomeUsuario=usuario).first()
			if (usuario_db):
				senha_db = usuario_db.senha
				ativo_db = usuario_db.ativo

				# Autenticação - Senha criptografada:
				# if (senha == senha_hashed):

				# Autenticação - Senha não criptografada:
				if (senha == senha_db):

					# Continuação:
					if (ativo_db == ativo):
						return "{} - {}".format(form.usuario.data, senha_hashed)
						# return (redirect("/home"))
					else:
						flash('Essa conta está inativa.', 'warning')
				else: 
					flash('A senha está incorreta. ', "danger")
					return redirect("/login")
			else: 
				flash('O nome de usuário não existe. ', "danger")
	return render_template('login.html', form=form)

@app.route('/registrar', methods=['GET','POST'])
def registrar():
	form = RegistrarForm()
	if form.validate_on_submit():
		
		# Adicionando ao banco de dados
		salt = bcrypt.gensalt(8)
		senha_hashed = bcrypt.hashpw(form.senha.data.encode('utf8'), salt)

		# Executa o comando:
		me = Usuario(form.usuario.data, form.email.data, senha_hashed, salt, 1)

		# Efetua um commit no banco de dados.
		# Por padrão, não é efetuado commit automaticamente. Você deve commitar para salvar
		# suas alterações.
		db.session.add(me)

		# Aqui pode pedir uma confirmação 
		db.session.commit()

		flash("Usuário registrado com sucesso!", "success")
		return (redirect("/login"))
	elif len(form.errors.items()) > 0:
		for campo, mensagens in form.errors.items():
 			for m in mensagens:
 				flash(m, "danger")
		return (redirect("/registrar"))

	return render_template("registrar.html", form=form)

@app.route('/logout')
def logout():
    return 'Logout'

@app.route('/home')
def home():
	return render_template('home.html', title='StudyFlow')