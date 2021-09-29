from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    usuario = StringField("usuario", validators=[InputRequired()])
    senha = PasswordField("senha", validators=[InputRequired()])
    entrar = SubmitField("entrar")
