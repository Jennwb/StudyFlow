from app import db

class Materia(db.Model):
    __tablename__="Matéria"
    codMateria = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.String(100))
    nome = db.Column(db.String(100))
    nivelAfinidade = db.Column(db.Integer(100))
    pesoProva = db.Column(db.Integer(100))

    def __init__(self, id_usuario, nome, nivelAfinidade, pesoProva):
        self.id_usuario = id_usuario
        self.nome = nome
        self.nivelAfinidade = nivelAfinidade
        self.pesoProva = pesoProva
        
    def __repr__(self):
        return "<Matéria: {}>".format(self.nome)