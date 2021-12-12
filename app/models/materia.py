from app import db

class Materia(db.Model):
    __tablename__="Matéria"
    codMateria = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.String(100))
    nome = db.Column(db.String(100))
    nivelAfinidade = db.Column(db.Integer)
    pesoProva = db.Column(db.Integer)

    def __init__(self, id_usuario, nome, nivel_afinidade, peso_prova):
        self.id_usuario = id_usuario
        self.nome = nome
        self.nivelAfinidade = nivel_afinidade
        self.pesoProva = peso_prova
        
    def __repr__(self):
        return "<Matéria: {}>".format(self.nome)