# from app import db

# class CicloDeEstudos(db.Model):
#     __tablename__="CicloDeEstudos"
#     id_usuario = db.Column(db.String(100))
#     nome_ciclo = db.Column(db.String(100))
#     # inicioCiclo = (pesquisar)
#     # fimCiclo = (pesquisar)
#     # horasDiarias = (pesquisar)
#     codCiclo = db.Column(db.Integer, primary_key=True)

#     def __init__(self, id_usuario, nome_ciclo, inicioCiclo, fimCiclo, horasDiarias):
#         self.id_usuario = id_usuario
#         self.nome_ciclo  = nome_ciclo
#         self.inicioCiclo = inicioCiclo
#         self.fimCiclo  = fimCiclo
#         self.horasDiarias = horasDiarias
        
#     def __repr__(self):
#         return "<Ciclo de estudos: {}>".format(self.nome)

# class Ciclo_Materia(db.Model):
#     __tablename__="CicloDeEstudos"
#     # horasDia_materia = (pesquisar)
#     codCiclo = db.Column(db.Integer)
#     codMateria = db.Column(db.Integer)

#     def __init__(self, codCiclo, codMateria, horasDia_materia):
#         self.codCiclo = codCiclo
#         self.codMateria  = codMateria
#         self.horasDia_materia = horasDia_materia
        
#     def __repr__(self):
#         return "<Ciclo e Matéria: {}>".format(self.codCiclo, self.codMateria)