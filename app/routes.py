from flask_login.utils import logout_user
from app import app
from flask import render_template
from flask import request, session
from flask import flash, redirect, url_for
from app.forms import LoginForm, RegistrarForm, AdicionarMaterias, EditarMaterias, AdicionarLembretes
from app.models.usuario import Usuario
from app.models.materia import Materia
from app.models.lembrete import Lembrete
# from app.models.ciclo import CicloDeEstudos, Ciclo_Materia
from app import db, lm
from flask_login import login_user, login_required, current_user
import bcrypt
from app import conexao

# User Loader
@lm.user_loader
def load_user(id_usuario):
    return Usuario.query.filter_by(id_usuario=id_usuario).first()

# Index
@app.route('/')
@app.route('/index')
def index():
	if not current_user.is_authenticated:
		return render_template('index.html', title='Study Flow')
	else:
		return render_template('home.html', title='Study Flow')

# Home
@app.route('/home')
def home():
    if not current_user.is_authenticated:
        flash('Apressadinho! Logue na sua conta primeiro.', 'warning')
        return redirect('/login')
    else:
        return render_template('home.html', title='Study Flow')

# Login
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
                        login_user(usuario_db)
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

# Cadastro
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    form = RegistrarForm()
    if form.validate_on_submit():
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

# Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')





# Matérias
@app.route('/materias')
def materias():
    if not current_user.is_authenticated:
        flash('Apressadinho! Logue na sua conta primeiro.', 'warning')
        return redirect('/login')
    else:
        id_usuario = current_user.get_id()
        materias_db = Materia.query.filter_by(id_usuario=id_usuario).all()
        return render_template('materias/listar_materia.html', title='Matérias', materias_db=materias_db)

# Matérias - adicionar
@app.route('/materias/adicionar', methods=['GET', 'POST'])
def adicionar():
    if not current_user.is_authenticated:
        flash('Apressadinho! Logue na sua conta primeiro.', 'warning')
        return redirect('/login')
    else:
        form = AdicionarMaterias()
        if form.validate_on_submit():
            id_usuario = current_user.get_id()
            nome = form.nome.data
            nivel_afinidade = form.nivel_afinidade.data
            peso_prova = form.peso_prova.data

            # Executa o comando:
            materia = Materia(id_usuario, nome, nivel_afinidade, peso_prova)

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

# Matérias - editar ----- NÃO PRONTO
@app.route('/editar/<codMateria>', methods=['GET', 'POST'])
def editar(codMateria):
	if not current_user.is_authenticated:
		flash('Apressadinho! Logue na sua conta primeiro.', 'warning')
		return redirect('/login')
	else:
		codMateria = codMateria
		materia = Materia.query.filter_by(codMateria=codMateria).first()
		id = materia.id_usuario
		if (current_user.get_id() == id):
			form = EditarMaterias()
			if form.validate_on_submit():
				# (materia.nome).update(dict(nome=form.nome.data))
				# (materia.nivelAfinidade).update(dict(nivelAfinidade=form.nivel_afinidade.data))
				# (materia.pesoProva).update(dict(pesoProva=form.peso_prova.data))

				materia = Materia.query.filter_by(codMateria=codMateria).first()
				materia.nome = form.nome.data
				# db.session.commit()
				materia.nivelAfinidade = form.nivel_afinidade.data
				# db.session.commit()
				materia.pesoProva = form.peso_prova.data
				# db.session.commit()

				# num_rows_updated = Materia.query.filter_by(codMateria=codMateria).update(dict(nome = form.nome.data, nivelAfinidade = form.nivel_afinidade.data, pesoProva = form.peso_prova.data))
				db.session.add(materia)
				db.session.commit()

	            # Aqui pode pedir uma confirmação
				

				flash("Matéria registrada com sucesso!", "success")
				return (redirect("/materias"))

			elif len(form.errors.items()) > 0:
				for campo, mensagens in form.errors.items():
					for m in mensagens:
						flash(m, "danger")
				return (redirect("/materias/editar_materia.html"))

			return render_template('/materias/editar_materia.html', form=form, materia=materia)

# Matérias - excluir
@app.route('/excluir/<codMateria>', methods=['GET', 'POST'])
def excluir(codMateria):
	if not current_user.is_authenticated:
		flash('Apressadinho! Logue na sua conta primeiro.', 'warning')
		return redirect('/login')
	else:
		codMateria = codMateria
		materia = Materia.query.filter_by(codMateria=codMateria).first()
		id = materia.id_usuario
		if (current_user.get_id() == id):
			materia = Materia.query.filter_by(codMateria=codMateria).first()
			db.session.delete(materia)
			db.session.commit()

			# Tem que colocar a mensagem de erro por causa da chave estrangeira do ciclo
			return (redirect("/materias"))





# Lembretes
@app.route('/lembretes')
def lembretes():
    if not current_user.is_authenticated:
        flash('Apressadinho! Logue na sua conta primeiro.', 'warning')
        return redirect('/login')
    else:
        id_usuario = current_user.get_id()
        lembretes = Lembrete.query.filter_by(id_usuario=id_usuario).all()
        return render_template('lembretes/listar_lembretes.html', title='Lembretes', lembretes=lembretes)

# Lembretes - adicionar
@app.route('/lembretes/adicionar', methods=['GET', 'POST'])
def adicionarL():
	if not current_user.is_authenticated:
		flash('Apressadinho! Logue na sua conta primeiro.', 'warning')
		return redirect('/login')
	else:
		form = AdicionarLembretes()
		if form.validate_on_submit():
			id_usuario = current_user.get_id()
			tipo = form.tipo.data
			nome = form.nome.data
			descricao = form.descricao.data
			data_hora = form.data_hora.data

			# Executa o comando:
			lembrete = Lembrete(id_usuario, tipo, nome, descricao, data_hora)

			# Efetua um commit no banco de dados.
			# Por padrão, não é efetuado commit automaticamente. Você deve commitar para salvar
			# suas alterações.
			db.session.add(lembrete)

			# Aqui pode pedir uma confirmação
			db.session.commit()

			flash("Lembrete registrado com sucesso!", "success")
			return (redirect("/lembretes"))

		elif len(form.errors.items()) > 0:
			for campo, mensagens in form.errors.items():
				for m in mensagens:
					flash(m, "danger")
			return (redirect("/lembretes/nova_materia.html"))

		return render_template('lembretes/nova_materia.html', form=form)

# Lembretes - editar ----- NÃO PRONTO
@app.route('/editar/<codLembrete>', methods=['GET', 'POST'])
def editarL(codLembrete):
	if not current_user.is_authenticated:
		flash('Apressadinho! Logue na sua conta primeiro.', 'warning')
		return redirect('/login')
	else:
		codLembrete = codLembrete
		materia = Materia.query.filter_by(codLembrete=codLembrete).first()
		id = materia.id_usuario
		if (current_user.get_id() == id):
			form = EditarMaterias()
			if form.validate_on_submit():
				# (materia.nome).update(dict(nome=form.nome.data))
				# (materia.nivelAfinidade).update(dict(nivelAfinidade=form.nivel_afinidade.data))
				# (materia.pesoProva).update(dict(pesoProva=form.peso_prova.data))

				materia = Materia.query.filter_by(codLembrete=codLembrete).first()
				materia.nome = form.nome.data
				# db.session.commit()
				materia.nivelAfinidade = form.nivel_afinidade.data
				# db.session.commit()
				materia.pesoProva = form.peso_prova.data
				# db.session.commit()

				# num_rows_updated = Materia.query.filter_by(codLembrete=codLembrete).update(dict(nome = form.nome.data, nivelAfinidade = form.nivel_afinidade.data, pesoProva = form.peso_prova.data))
				db.session.merge(materia)
				db.session.flush()
				db.session.commit()

	            # Aqui pode pedir uma confirmação
				

				flash("Matéria registrada com sucesso!", "success")
				return (redirect("/lembretes"))

			elif len(form.errors.items()) > 0:
				for campo, mensagens in form.errors.items():
					for m in mensagens:
						flash(m, "danger")
				return (redirect("/lembretes/editar_materia.html"))

			return render_template('/lembretes/editar_materia.html', form=form, materia=materia)

# Lembretes - excluir
@app.route('/excluir/<codLembrete>', methods=['GET', 'POST'])
def excluirL(codLembrete):
	if not current_user.is_authenticated:
		flash('Apressadinho! Logue na sua conta primeiro.', 'warning')
		return redirect('/login')
	else:
		codLembrete = codLembrete
		lembrete = Lembrete.query.filter_by(codLembrete=codLembrete).first()
		id = lembrete.id_usuario
		if (current_user.get_id() == id):
			db.session.delete(lembrete)
			db.session.commit()
			
			return (redirect("/lembretes"))















# Ciclo de Estudos
@app.route('/ciclos')
def ciclos():
    if not current_user.is_authenticated:
        flash('Apressadinho! Logue na sua conta primeiro.', 'warning')
        return redirect('/login')
    else:
        id_usuario = current_user.get_id()
        ciclo = CicloDeEstudos.query.filter_by(id_usuario=id_usuario).all()
        return render_template('ciclo/listar_ciclo.html', title='Ciclo de Estudos', ciclo=ciclo)