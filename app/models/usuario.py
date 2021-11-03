from app import db
from app import conexao

class Usuario(db.Model):
    __tablename__="Usuário"
    id_usuario = db.Column(db.Integer, primary_key=True)
    nomeUsuario = db.Column(db.String(100))
    email = db.Column(db.String(100))
    senha = db.Column(db.String(100))
    salt = db.Column(db.String(100))
    ativo = db.Column(db.String(100))

    def __init__(self, nome, email, senha, salt, ativo):
        self.nomeUsuario = nome
        self.email = email
        self.senha = senha
        self.salt = salt
        self.ativo = ativo
        
    def __repr__(self):
        return "<Usuario: {}>".format(self.nome)