from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models.users import Users
from utils.db import db

register = Blueprint("register", __name__)


@register.route("/register", methods=["POST"])
def registrar(data=None):

    if data is None:
        data = request.get_json()

    # Verificar si el usuario ya existe
    existing_user = Users.query.filter_by(username=data["username"]).first()
    if existing_user:
        response = jsonify({"message": "User already exists"})
        response.status_code = 409  # 409 Conflict
        return response

    # Hashear la contraseña
    hashed_password = generate_password_hash(
        data["password"], method="pbkdf2:sha256", salt_length=8
    )

    # Crear un nuevo usuario
    new_user = Users(
        username=data["username"], password=hashed_password, rol=data["rol"]
    )
    db.session.add(new_user)
    db.session.commit()

    response = jsonify({"message": "User created successfully"})
    response.status_code = 201
    return response



