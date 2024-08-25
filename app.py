from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from routes.pacientes import pacientes
from routes.medicos import medicos
from routes.auth import routes_auth
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
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    },
)

# Register the blueprint
app.register_blueprint(pacientes)
app.register_blueprint(routes_auth)
app.register_blueprint(medicos)

# Ensure models are imported after db.init_app(app)
with app.app_context():
    # from models.paciente import Paciente
    db.create_all()
