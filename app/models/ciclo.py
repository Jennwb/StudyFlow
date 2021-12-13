from app import db

class CicloDeEstudos(db.Model):
    __tablename__="CicloDeEstudos"
    id_usuario = db.Column(db.String(100))
    nome_ciclo = db.Column(db.String(100))
    inicioCiclo = db.Column(db.Date)
    fimCiclo = db.Column(db.Date)
    horasDiarias = db.Column(db.Integer)
    codCiclo = db.Column(db.Integer, primary_key=True)

    def __init__(self, id_usuario, nome_ciclo, inicioCiclo, fimCiclo, horasDiarias):
        self.id_usuario = id_usuario
        self.nome_ciclo  = nome_ciclo
        self.inicioCiclo = inicioCiclo
        self.fimCiclo  = fimCiclo
        self.horasDiarias = horasDiarias
        
    def __repr__(self):
        return "<Ciclo de estudos: {}>".format(self.nome)

class Ciclo_Materia(db.Model):
    __tablename__="Ciclo_Materia"
    horasDia_materia = db.Column(db.Float)
    codCiclo = db.Column(db.Integer, db.ForeignKey("CicloDeEstudos.codCiclo"), primary_key=True)
    codMateria = db.Column(db.Integer, db.ForeignKey("Materia.codMateria"), primary_key=True)

    def __init__(self, codCiclo, codMateria, hr_m):
        self.codCiclo = codCiclo
        self.codMateria  = codMateria
        self.horasDia_materia = hr_m
        
    def __repr__(self):
        return "<Ciclo e Matéria: {}>".format(self.codCiclo, self.codMateria)