from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Email, EqualTo, AnyOf
from wtforms.fields.html5 import EmailField, DateTimeField

class LoginForm(FlaskForm):
    usuario = StringField("usuario", validators=[InputRequired()])
    senha = PasswordField("senha", validators=[InputRequired()])
    entrar = SubmitField("Entrar")

class RegistrarForm(FlaskForm):
    usuario = StringField("usuario", validators=[InputRequired()])
    email = EmailField("email", validators=[InputRequired(), Email()])
    senha = PasswordField("senha", validators=[InputRequired(), EqualTo("confirmarsenha", message="As senhas não conferem.")])
    confirmarsenha = PasswordField("confirmarsenha", validators=[InputRequired()])
    registrar = SubmitField("Cadastrar")

class AdicionarMaterias(FlaskForm):
    nome = StringField("nome", validators=[InputRequired()])
    nivel_afinidade = SelectField('nivel_afinidade', choices=[('', 'Selecione sua afinidade com a matéria:'), ('1', 'Muito baixo'), ('2', 'Baixo'), ('3', 'Neutro'), ('4', 'Alto'), ('5', 'Muito alto')], validators=[InputRequired()])
    peso_prova = SelectField('peso_prova', choices=[('', 'Selecione o peso da matéria na prova:'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[InputRequired()])
    adicionar = SubmitField("Pronto!")

class EditarMaterias(FlaskForm):
    nome = StringField("nome", validators=[InputRequired()])
    nivel_afinidade = SelectField('nivel_afinidade', choices=[('', 'Selecione sua afinidade com a matéria:'), ('1', 'Muito baixo'), ('2', 'Baixo'), ('3', 'Neutro'), ('4', 'Alto'), ('5', 'Muito alto')], validators=[InputRequired()])
    peso_prova = SelectField('peso_prova', choices=[('', 'Selecione o peso da matéria na prova:'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[InputRequired()])
    adicionar = SubmitField("Pronto!")

class AdicionarLembretes(FlaskForm):
    nome = StringField("nome", validators=[InputRequired()])
    descricao = StringField("descricao", validators=[InputRequired()])
    tipo = SelectField('tipo', choices=[('', 'Selecione o tipo de lembrete:'), ('0', 'Lembrete de Estudos'), ('1', 'Lembrete da Prova')], validators=[InputRequired()])
    data_hora = DateTimeField('data_hora', format='%Y-%m-%d %H:%M:%S', validators=[InputRequired()])
    adicionar = SubmitField("Pronto!")
    
class EditarLembretes(FlaskForm):
    nome = StringField("nome", validators=[InputRequired()])
    descricao = StringField("descricao", validators=[InputRequired()])
    tipo = SelectField('tipo', choices=[('', 'Selecione o tipo de lembrete:'), ('0', 'Lembrete de Estudos'), ('1', 'Lembrete da Prova')], validators=[InputRequired()])
    data_hora = DateTimeField('data_hora', format='%Y-%m-%d %H:%M:%S', validators=[InputRequired()])
    adicionar = SubmitField("Pronto!")