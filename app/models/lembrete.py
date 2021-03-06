from app import db

class Lembrete(db.Model):
    __tablename__="Lembrete"
    id_usuario = db.Column(db.String(100))
    tipoLembrete = db.Column(db.String(100))
    nomeLembrete = db.Column(db.String(100))
    descricao = db.Column(db.String(500))
    data_horaLembrete = db.Column(db.DateTime)
    codLembrete = db.Column(db.Integer, primary_key=True)

    def __init__(self, id_usuario, tipo, nome, descricao, data_hora):
        self.id_usuario = id_usuario
        self.tipoLembrete = tipo
        self.nomeLembrete = nome
        self.descricao = descricao
        self.data_horaLembrete = data_hora
        
    def __repr__(self):
        return "<Lembrete: {}>".format(self.nome)