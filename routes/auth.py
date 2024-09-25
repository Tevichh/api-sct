from re import split
from flask import Blueprint, request, jsonify
from f_jwt import write_token, validate_token
from werkzeug.security import check_password_hash
from models.users import Users

routes_auth = Blueprint("routes_auth", __name__)

@routes_auth.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    # Consulta en la base de datos
    user = Users.query.filter_by(username=data["username"]).first()

    # Verificación de usuario y contraseña
    if user and check_password_hash(
        user.password, data["password"]
    ):  # user.password == data['password']
        token = write_token(data={"username": user.username})
        return (
            jsonify(
                {"token": token, "user": user.username, "isTrue": True, "rol": user.rol}
            ),
            200,
        )
    else:
        return (
            jsonify(
                {"message": "User not found or incorrect password", "isTrue": False}
            ),
            200,
        )


@routes_auth.route("/verify/token")
def verify():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return (
            jsonify({"message": "Token de autenticación faltante o mal formado"}),
            401,
        )

    token = auth_header.split(" ")[1]

    return validate_token(token, output=True)
