from utils.db import db

class Paciente(db.Model):
    __tablename__ = "Paciente"

    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    tipo_id = db.Column(db.String(50), nullable=False)
    num_paciente_id = db.Column(db.String(50), unique=True, nullable=False)
    nombre_1 = db.Column(db.String(100), nullable=False)
    nombre_2 = db.Column(db.String(100))
    apellido_1 = db.Column(db.String(100), nullable=False)
    apellido_2 = db.Column(db.String(100))
    pais = db.Column(db.String(100), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    num_telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __init__(self, tipo_id, num_paciente_id, nombre_1, nombre_2, apellido_1, apellido_2, pais, ciudad, direccion, fecha_nacimiento, num_telefono, email):
        self.tipo_id = tipo_id
        self.num_paciente_id = num_paciente_id
        self.nombre_1 = nombre_1
        self.nombre_2 = nombre_2
        self.apellido_1 = apellido_1
        self.apellido_2 = apellido_2
        self.pais = pais
        self.ciudad = ciudad
        self.direccion = direccion
        self.fecha_nacimiento = fecha_nacimiento
        self.num_telefono = num_telefono
        self.email = email

