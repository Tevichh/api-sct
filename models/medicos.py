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
