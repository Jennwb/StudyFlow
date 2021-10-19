from app import app
from flask import render_template
from flask import request
from flask import flash, redirect
from app.forms import LoginForm, RegistrarForm
from app.models.usuario import Usuario
from app import db

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

@app.route('/registrar', methods=['GET','POST'])
def registrar():
    form = RegistrarForm()
    if form.validate_on_submit():
        flash("Usuário registrado com sucesso!", "success")
        return (redirect("/registrar"))
    elif len(form.errors.items()) > 0:
        for campo, mensagens in form.errors.items():
            for m in mensagens:
                flash(m, "danger")
        return (redirect("/registrar"))

    return render_template("registrar.html", form=form)

@app.route('/home')
def home():
	return render_template('home.html', title='StudyFlow')