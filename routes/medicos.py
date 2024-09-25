from flask import Blueprint, jsonify, request
from models.medicos import Medico
from models.users import Users
from utils.db import db
from f_jwt import validate_token
from .register import registrar

medicos = Blueprint("medicos", __name__)


@medicos.before_request
def validar_token():
    # Permitir solicitudes OPTIONS sin autenticación
    if request.method == "OPTIONS":
        return "", 200

    # Obtener el encabezado de autorización
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return (
            jsonify({"message": "Token de autenticación faltante o mal formado"}),
            401,
        )

    token = auth_header.split(" ")[1]
    return validate_token(token, output=False)


# METODO GET


@medicos.route("/medicos", methods=["GET"])
def get_medicos():
    medicos = Medico.query.all()
    medicos_list = []
    for medico in medicos:
        medico_dict = {
            "tipo_id": medico.tipo_id,
            "num_medico_id": medico.num_medico_id,
            "nombre_1": medico.nombre_1,
            "nombre_2": medico.nombre_2,
            "apellido_1": medico.apellido_1,
            "apellido_2": medico.apellido_2,
            "num_telefono": medico.num_telefono,
            "email": medico.email,
        }
        medicos_list.append(medico_dict)
    return jsonify(medicos_list)


# METODO POST
@medicos.route("/medicos", methods=["POST"])
def add_medico():
    data = request.get_json()

    userName = (
        data["nombre_1"][0].lower()
        + (data["nombre_2"][0].lower() if data["nombre_2"] else "")
        + data["apellido_1"].lower()
        + (data["apellido_2"][0].lower() if data["apellido_2"] else "")
    )

    user_data = {
        "username": userName,
        "password": data["num_medico_id"],
        "rol": "Medico",
    }

    print(userName)

    response = registrar(user_data)

    if response.status_code == 409:
        return response

    new_medico = Medico(
        tipo_id=data["tipo_id"],
        num_medico_id=data["num_medico_id"],
        nombre_1=data["nombre_1"],
        nombre_2=data["nombre_2"],
        apellido_1=data["apellido_1"],
        apellido_2=data["apellido_2"],
        num_telefono=data["num_telefono"],
        email=data["email"],
        user=userName,
    )

    db.session.add(new_medico)
    db.session.commit()
    return (
        jsonify(
            {
                "tipo_id": new_medico.tipo_id,
                "num_medico_id": new_medico.num_medico_id,
                "nombre_1": new_medico.nombre_1,
                "nombre_2": new_medico.nombre_2,
                "apellido_1": new_medico.apellido_1,
                "apellido_2": new_medico.apellido_2,
                "num_telefono": new_medico.num_telefono,
                "email": new_medico.email,
                "user": new_medico.user,
            }
        ),
        201,
    )


# METODO PUT (UPDATE)


@medicos.route("/medicos/<string:identificador>", methods=["PUT"])
def update_medico(identificador):
    data = request.get_json()
    medico = Medico.query.filter_by(num_medico_id=identificador).first()
    if not medico:
        return jsonify({"message": "Medico not found"}), 404

    medico.tipo_id = data.get("tipo_id", medico.tipo_id)
    medico.nombre_1 = data.get("nombre_1", medico.nombre_1)
    medico.nombre_2 = data.get("nombre_2", medico.nombre_2)
    medico.apellido_1 = data.get("apellido_1", medico.apellido_1)
    medico.apellido_2 = data.get("apellido_2", medico.apellido_2)
    medico.num_telefono = data.get("num_telefono", medico.num_telefono)
    medico.email = data.get("email", medico.email)
    db.session.commit()
    return jsonify(
        {
            "tipo_id": medico.tipo_id,
            "num_medico_id": medico.num_medico_id,
            "nombre_1": medico.nombre_1,
            "nombre_2": medico.nombre_2,
            "apellido_1": medico.apellido_1,
            "apellido_2": medico.apellido_2,
            "num_telefono": medico.num_telefono,
            "email": medico.email,
        }
    )


# METODO DELETE


@medicos.route("/medicos/<string:identificador>", methods=["DELETE"])
def delete_medico(identificador):

    medico = Medico.query.filter_by(num_medico_id=identificador).first()
    if not medico:
        return jsonify({"message": "Medico not found"}), 404

    usuario = Users.query.filter_by(username=medico.user).first()
    if not usuario:

        db.session.delete(medico)
        db.session.commit()
        return (
            jsonify({"message": "Medico deleted successfully, but user not found"}),
            200,
        )

    db.session.delete(medico)
    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"message": "Medico and associated user deleted successfully"})
