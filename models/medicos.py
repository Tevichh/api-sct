from utils.db import db


class Medico(db.Model):
    __tablename__ = "Medico"
    id = db.Column(
        db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True
    )
    tipo_id = db.Column(db.String(50), nullable=False)
    num_medico_id = db.Column(db.String(50), unique=True, nullable=False)
    nombre_1 = db.Column(db.String(100), nullable=False)
    nombre_2 = db.Column(db.String(100))
    apellido_1 = db.Column(db.String(100), nullable=False)
    apellido_2 = db.Column(db.String(100))
    num_telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    user = db.Column(db.String(100), nullable=False)

    def __init__(
        self,
        tipo_id,
        num_medico_id,
        nombre_1,
        nombre_2,
        apellido_1,
        apellido_2,
        num_telefono,
        email,
        user
    ):
        self.tipo_id = tipo_id
        self.num_medico_id = num_medico_id
        self.nombre_1 = nombre_1
        self.nombre_2 = nombre_2
        self.apellido_1 = apellido_1
        self.apellido_2 = apellido_2
        self.num_telefono = num_telefono
        self.email = email
        self.user = user
