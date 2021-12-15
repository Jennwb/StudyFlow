from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import InputRequired, Email, EqualTo, NumberRange
from wtforms.fields import EmailField, DateTimeField, DateField, IntegerField, SelectField
import datetime

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
    data_hora = DateTimeField('data_hora', validators=[InputRequired()], format='%d-%m-%Y %H:%M:%S')
    adicionar = SubmitField("Pronto!")
    
class EditarLembretes(FlaskForm):
    nome = StringField("nome", validators=[InputRequired()])
    descricao = StringField("descricao", validators=[InputRequired()])
    tipo = SelectField('tipo', choices=[('', 'Selecione o tipo de lembrete:'), ('0', 'Lembrete de Estudos'), ('1', 'Lembrete da Prova')], validators=[InputRequired()])
    data_hora = DateTimeField('data_hora', validators=[InputRequired()], format='%d-%m-%Y %H:%M:%S')
    adicionar = SubmitField("Pronto!")

class AdicionarCiclos(FlaskForm):

    # CHECAR SE AS DATAS FAZEM SENTIDO

    # def checar_datas(form, field):
    #         result = super(AdicionarCiclos, field).validate()
    #         if (field.startdate.data>field.enddate.data):
    #             return False
    #         else:
    #             return result
                
    nome = StringField("nome", validators=[InputRequired()])

    data_inicial = DateField('data_inicial', default=datetime.date.today, validators=[InputRequired()], format='%Y-%m-%d',)
    data_final = DateField('data_final', default=datetime.date.today, validators=[InputRequired()], format='%Y-%m-%d')
    # data_inicial = DateField('data_inicial', default=datetime.date.today, validators=[InputRequired()], format='%d-%m-%Y',)
    # data_final = DateField('data_final', default=datetime.date.today, validators=[InputRequired()], format='%d-%m-%Y')

    horas_semanais = IntegerField("horas_semanais", validators=[InputRequired(), NumberRange(min=1, max=168, message="Coloque um número de horas realista")], default="1")

    # Depois transformar em checkbox
    materias = SelectMultipleField('materias', choices=[(1, 'Label 1'), (1000, 'Label 2')], coerce=int, validators=[InputRequired()])
    # materias = SelectMultipleField('materias', choices=[], validators=[InputRequired()])
    adicionar = SubmitField("Pronto!")

    