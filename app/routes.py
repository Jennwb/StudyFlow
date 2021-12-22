# from types import NoneType
from flask_login.utils import logout_user
from app import app
from flask import render_template
from flask import request, session
from flask import flash, redirect, url_for
from app.forms import LoginForm, RegistrarForm, AdicionarMaterias, EditarMaterias, AdicionarLembretes, EditarLembretes, AdicionarCiclos, EditarCiclo
from app.models.usuario import Usuario
from app.models.materia import Materia
from app.models.lembrete import Lembrete
from app.models.ciclo import CicloDeEstudos, Ciclo_Materia
from app import db, lm
from flask_login import login_user, login_required, current_user
import bcrypt
from app import conexao
import sys

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
		return (redirect(url_for('home')))
		
# Home
@app.route('/home')
def home():
	if not current_user.is_authenticated:
		flash('Apressadinho! Logue na sua conta primeiro.', 'warning')
		return redirect('/login')
	else:
		id = current_user.get_id()
		ciclo = CicloDeEstudos.query.filter_by(id_usuario=id).first()
		if 'ciclo.codCiclo' in locals():
			return render_template('home.html', title='Study Flow')			
		else:
			codCiclo = ciclo.codCiclo
			Ciclo_m = Ciclo_Materia.query.filter_by(codCiclo=codCiclo).all()

			materias = []
			minutos = []

			for cd in Ciclo_m:
				m = Materia.query.filter_by(codMateria=cd.codMateria).first()
				materias.append(m.nome)
			for c in Ciclo_m:
				d = Ciclo_Materia.query.filter_by(codCiclo=codCiclo, codMateria=c.codMateria).first()
				minutos.append(d.horasDia_materia)
			return render_template('home.html', title='Study Flow', ciclo=ciclo, materias=materias, minutos=minutos)





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

# Matérias - editar
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
			form = EditarMaterias(nome=materia.nome, nivel_afinidade=materia.nivelAfinidade, peso_prova=materia.pesoProva)
			if form.validate_on_submit():
				materia = Materia.query.filter_by(codMateria=codMateria).first()
				materia.nome = form.nome.data
				materia.nivelAfinidade = form.nivel_afinidade.data
				materia.pesoProva = form.peso_prova.data
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
			return (redirect("/lembretes/novo_lembrete.html"))

		return render_template('lembretes/novo_lembrete.html', form=form)

# Lembretes - editar
@app.route('/lembretes/editar/<codLembrete>', methods=['GET', 'POST'])
def editarL(codLembrete):
	if not current_user.is_authenticated:
		flash('Apressadinho! Logue na sua conta primeiro.', 'warning')
		return redirect('/login')
	else:
		codLembrete = codLembrete
		lembrete = Lembrete.query.filter_by(codLembrete=codLembrete).first()
		id = lembrete.id_usuario
		if (current_user.get_id() == id):
			form = EditarLembretes(nome=lembrete.nomeLembrete, descricao=lembrete.descricao, tipo=lembrete.tipoLembrete, data_hora=lembrete.data_horaLembrete)
			if form.validate_on_submit():
				lembrete = Lembrete.query.filter_by(codLembrete=codLembrete).first()
				lembrete.nomeLembrete = form.nome.data
				lembrete.tipoLembrete = form.tipo.data
				lembrete.descricao = form.descricao.data
				lembrete.data_horaLembrete = form.data_hora.data
				db.session.add(lembrete)
				db.session.commit()

	            # Aqui pode pedir uma confirmação

				flash("Lembrete registrado com sucesso!", "success")
				return (redirect("/lembretes"))

			elif len(form.errors.items()) > 0:
				for campo, mensagens in form.errors.items():
					for m in mensagens:
						flash(m, "danger")
				return (redirect("/lembretes/editar_lembrete.html"))

			return render_template('/lembretes/editar_lembrete.html', form=form, lembrete=lembrete)

# Lembretes - excluir
@app.route('/lembretes/excluir/<codLembrete>', methods=['GET', 'POST'])
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





# Ciclos - adicionar
@app.route('/ciclos/adicionar', methods=['GET', 'POST'])
def adicionarC():
	if not current_user.is_authenticated:
		flash('Apressadinho! Logue na sua conta primeiro.', 'warning')
		return redirect('/login')
	else:
		id_usuario = current_user.get_id()
		form = AdicionarCiclos()
		form.materias.choices = [(row.codMateria, row.nome) for row in Materia.query.filter_by(id_usuario=id_usuario).all()]

		if form.validate_on_submit():
			nome = form.nome.data
			data_inicial = form.data_inicial.data
			data_final = form.data_final.data
			horas_semanais = form.horas_semanais.data
			materias = form.materias.data
			
			minutos_diarios = horas_semanais*60

			# Executa o comando:
			ciclo = CicloDeEstudos(id_usuario, nome, data_inicial, data_final, horas_semanais)

			# Efetua um commit no banco de dados.
			# Por padrão, não é efetuado commit automaticamente. Você deve commitar para salvar
			# suas alterações.
			db.session.add(ciclo)

			# Aqui pode pedir uma confirmação
			db.session.commit()

			ultimo = materias.pop()
			materias.append(ultimo)
			n_indices = ultimo + 2

			peso_final = [] * n_indices
			media_m = [] * n_indices
			hr_m = 0
			
			for m in materias:
				materia_db = Materia.query.filter_by(codMateria=m).first()
				peso_prova = materia_db.pesoProva
				nivel_afinidade = materia_db.nivelAfinidade

				peso_final.insert(m, peso_prova + nivel_afinidade)

			peso_total = sum(peso_final)
			
			for ma in materias:
				materias.reverse()

				pf = peso_final.pop()
				media_m.insert(ma, (pf / peso_total))
				mm = media_m.pop()
				hr_m = mm * minutos_diarios
				c_m = Ciclo_Materia(ciclo.codCiclo, ma, hr_m)
				db.session.add(c_m)
				db.session.commit()
				materias.reverse()

			flash("Ciclo de estudos registrado com sucesso!", "success")
			return redirect(url_for('ciclos', codCiclo=ciclo.codCiclo))

		elif len(form.errors.items()) > 0:
			for campo, mensagens in form.errors.items():				
				for m in mensagens:
					flash(m, "danger")
			return (redirect("/ciclos/adicionar"))

		return render_template('ciclodeestudos/novo_ciclo.html', form=form)

# Ciclo de Estudos
@app.route('/ciclos/<codCiclo>', methods=['GET', 'POST'])
def ciclos(codCiclo):
	if not current_user.is_authenticated:
		flash('Apressadinho! Logue na sua conta primeiro.', 'warning')
		return redirect('/login')
	else:
		id_usuario = current_user.get_id()
		ciclo = CicloDeEstudos.query.filter_by(id_usuario=id_usuario, codCiclo=codCiclo).first()
		if 'ciclo.codCiclo' in locals():
			codMaterias = Ciclo_Materia.query.filter_by(codCiclo=codCiclo).all()

			materias = []
			minutos = []

			for cd in codMaterias:
				m = Materia.query.filter_by(c=cd).first()
				materias = m.nome
			for c in codMaterias:
				d = codMaterias = Ciclo_Materia.query.filter_by(codCiclo=codCiclo, c=c).first()
				minutos = d.horasDia_materia
					
			return render_template('ciclodeestudos/detalhes_ciclo.html', title='Ciclo de Estudos', ciclo=ciclo, materias=materias, minutos=minutos)			
		else:
			# flash('Não há ciclos cadastrados.', 'warning')
			# return redirect('/home')
			codCiclo = ciclo.codCiclo
			Ciclo_m = Ciclo_Materia.query.filter_by(codCiclo=codCiclo).all()

			materias = []
			minutos = []

			for cd in Ciclo_m:
				m = Materia.query.filter_by(codMateria=cd.codMateria).first()
				materias.append(m.nome)
			for c in Ciclo_m:
				d = Ciclo_Materia.query.filter_by(codCiclo=codCiclo, codMateria=c.codMateria).first()
				minutos.append(d.horasDia_materia)
					
			return render_template('ciclodeestudos/detalhes_ciclo.html', title='Ciclo de Estudos', ciclo=ciclo, materias=materias, minutos=minutos)

# Ciclos - editar
@app.route('/ciclos/editar/<codCiclo>', methods=['GET', 'POST'])
def editarC(codCiclo):
	if not current_user.is_authenticated:
		flash('Apressadinho! Logue na sua conta primeiro.', 'warning')
		return redirect('/login')
	else:
		codCiclo = codCiclo
		ciclo = CicloDeEstudos.query.filter_by(codCiclo=codCiclo).first()
		c_m = Ciclo_Materia.query.filter_by(codCiclo=codCiclo).all()
		default_m = [] * len(c_m)
		for cm in c_m:
			default_m.append(cm.codMateria)
		id = ciclo.id_usuario
		
		if (current_user.get_id() == id):
			form = EditarCiclo(nome=ciclo.nome_ciclo, data_inicial=ciclo.inicioCiclo, data_final=ciclo.fimCiclo, horas_semanais=ciclo.horasDiarias, materias=default_m)
			form.materias.choices = [(row.codMateria, row.nome) for row in Materia.query.filter_by(id_usuario=id).all()]
			if form.validate_on_submit():
				ciclo = CicloDeEstudos.query.filter_by(codCiclo=codCiclo).first()
				ciclo.nome_ciclo = form.nome.data
				ciclo.inicioCiclo = form.data_inicial.data
				ciclo.fimCiclo = form.data_final.data
				ciclo.horasDiarias = form.horas_semanais.data

				db.session.add(ciclo)
				db.session.commit()

				horas_semanais = form.horas_semanais.data
				materias = form.materias.data

				minutos_diarios = horas_semanais*60

				ultimo = materias.pop()
				materias.append(ultimo)
				n_indices = ultimo + 2

				peso_final = [] * n_indices
				media_m = [] * n_indices
				hr_m = 0
				
				for m in materias:
					materia_db = Materia.query.filter_by(codMateria=m).first()
					peso_prova = materia_db.pesoProva
					nivel_afinidade = materia_db.nivelAfinidade

					peso_final.insert(m, peso_prova + nivel_afinidade)

				peso_total = sum(peso_final)

				# Limpando tabela Ciclo_Materia
				ciclo_materia_e = Ciclo_Materia.query.filter_by(codCiclo=codCiclo).all()
				for cme in ciclo_materia_e:
					db.session.delete(cme)
					db.session.commit()
				
				for ma in materias:
					materias.reverse()

					pf = peso_final.pop()
					media_m.insert(ma, (pf / peso_total))
					mm = media_m.pop()
					hr_m = mm * minutos_diarios
					c_m = Ciclo_Materia(ciclo.codCiclo, ma, hr_m)
					db.session.add(c_m)
					db.session.commit()
					materias.reverse()

	            # Aqui pode pedir uma confirmação

				flash("Ciclo de estudos atualizado com sucesso!", "success")
				return redirect(url_for('ciclos', codCiclo=ciclo.codCiclo))

			elif len(form.errors.items()) > 0:
				for campo, mensagens in form.errors.items():
					for m in mensagens:
						flash(m, "danger")
				return (redirect("/ciclodeestudos/editar_ciclo.html"))

			return render_template('/ciclodeestudos/editar_ciclo.html', form=form, ciclo=ciclo)

# Ciclos - excluir
@app.route('/ciclos/excluir/<codCiclo>', methods=['GET', 'POST'])
def excluirC(codCiclo):
	if not current_user.is_authenticated:
		flash('Apressadinho! Logue na sua conta primeiro.', 'warning')
		return redirect('/login')
	else:
		codCiclo = codCiclo
		ciclo = CicloDeEstudos.query.filter_by(codCiclo=codCiclo).first()
		c_m = Ciclo_Materia.query.filter_by(codCiclo=codCiclo).all()
		id = ciclo.id_usuario
		if (current_user.get_id() == id):
			for cm in c_m:
				db.session.delete(cm)
				db.session.commit()

			db.session.delete(ciclo)
			db.session.commit()
			
			return (redirect("/home"))