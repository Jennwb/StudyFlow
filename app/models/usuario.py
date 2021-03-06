from app import db

class Usuario(db.Model):
    __tablename__="Usuário"
    id_usuario = db.Column(db.Integer, primary_key=True)
    nomeUsuario = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.LargeBinary(100), nullable=False)
    # salt = db.Column(db.LargeBinary(8), nullable=False)
    ativo = db.Column(db.Integer(), nullable=False)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        id = int(self.id_usuario)
        return id

    def __init__(self, nome, email, senha, salt, ativo):
        self.nomeUsuario = nome
        self.email = email
        self.senha = senha
        self.salt = salt
        self.ativo = ativo
        
    def __repr__(self):
        return "<Usuario: {}>".format(self.nomeUsuario)