from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from routes.pacientes import pacientes
from routes.medicos import medicos
from routes.auth import routes_auth
from routes.register import register
from routes.consultas import consulta
from utils.db import db
from config import DATABASE_CONECTION_URI

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Configura CORS
CORS(
    app,
    resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Incluye OPTIONS
            "allow_headers": ["Content-Type", "Authorization"],
        }
    },
)


# Register the blueprint
app.register_blueprint(pacientes)
app.register_blueprint(routes_auth)
app.register_blueprint(medicos)
app.register_blueprint(register)
app.register_blueprint(consulta)

# Ensure models are imported after db.init_app(app)
with app.app_context():
    # from models.paciente import Paciente
    db.create_all()

    from models.users import Users
    from werkzeug.security import generate_password_hash

    admin_user = Users.query.filter_by(username="Admin").first()

    if not admin_user:
        # Hashear la contraseña
        hashed_password = generate_password_hash(
            "00000000", method="pbkdf2:sha256", salt_length=8
        )
        # Crear el nuevo usuario Admin
        new_admin = Users(username="Admin", password=hashed_password, rol="Admin")
        db.session.add(new_admin)
        db.session.commit()
