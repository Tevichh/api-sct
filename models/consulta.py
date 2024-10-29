from utils.db import db


class Consulta(db.Model):

    __tablename__ = "Consulta"
    id = db.Column(
        db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True
    )

    identificacion = db.Column(db.String(50), nullable=False)
    nombreCompleto = db.Column(db.String(300), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    muestraUrl = db.Column(db.String(100), nullable=False)
    resultado = db.Column(db.String(100), nullable=False)
    observaciones = db.Column(db.String(1000), nullable=False)
    medico = db.Column(db.String(300), nullable=False)

    def __init__(
        self,
        identificacion,
        nombreCompleto,
        fecha,
        muestraUrl,
        resultado,
        observaciones,
        medico,
    ):
        self.identificacion = identificacion
        self.nombreCompleto = nombreCompleto
        self.fecha = fecha
        self.muestraUrl = muestraUrl
        self.resultado = resultado
        self.observaciones = observaciones
        self.medico = medico
