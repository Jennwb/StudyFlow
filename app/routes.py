from app import app
from flask import render_template
from flask import request
from flask import flash, redirect
from app.forms import LoginForm, RegistrarForm, AdicionarMaterias
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
		senha = form.senha.data.encode('utf8')
		ativo = 1

	# Autenticação
		if usuario == 'admin' and senha == 'admin':
			return "{} - {}".format(form.usuario.data, form.senha.data)
		else:
			usuario_db = Usuario.query.filter_by(nomeUsuario=usuario).first()
			if (usuario_db):
				ativo_db = usuario_db.ativo
				senha_db = usuario_db.senha

				auth = bcrypt.checkpw(senha, senha_db)
				if (auth):
					if (ativo_db == ativo):
						return (redirect("/home"))
					else:
						flash('Essa conta está inativa.', 'warning')
				else: 
					flash('A senha está incorreta. ', "danger")
					return redirect("/login")
			else: 
				flash('O nome de usuário não existe. ', "danger")
				return redirect("/login")
	return render_template('login.html', form=form)

@app.route('/registrar', methods=['GET','POST'])
def registrar():
	form = RegistrarForm()
	if form.validate_on_submit():
		# Adicionando ao banco de dados
		salt = bcrypt.gensalt(8)
		senha_encoded = form.senha.data.encode('utf8')
		senha_hashed = bcrypt.hashpw(senha_encoded, salt)

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

@app.route('/materias')
def materias():
	return render_template('materias/listar_materia.html', title='Matérias')

@app.route('/materias/adicionar', methods=['GET','POST'])
def adicionar():
	form = AdicionarMaterias()
	if form.validate_on_submit():
		nome = form.nome.data
		nivel_afinidade = form.nivel_afinidade
		peso_prova = form.peso_prova

		materia = Usuario(id_usuario, nome, nivel_afinidade, peso_prova)

		# Efetua um commit no banco de dados.
		# Por padrão, não é efetuado commit automaticamente. Você deve commitar para salvar
		# suas alterações.
		db.session.add(materia)

		# Aqui pode pedir uma confirmação 
		db.session.commit()

		flash("Matéria registrada com sucesso!", "success")
		return (redirect("/materias"))

	elif len(form.errors.items()) > 0:
		for campo, mensagens in form.errors.items():
		 	for m in mensagens:
 				flash(m, "danger")
		return (redirect("/materias/nova_materia.html"))

	return render_template('materias/nova_materia.html', form=form)