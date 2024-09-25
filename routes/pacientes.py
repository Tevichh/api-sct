from flask import Blueprint, jsonify, request
from models.paciente import Paciente
from utils.db import db
from f_jwt import validate_token

pacientes = Blueprint("pacientes", __name__)


@pacientes.before_request
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


@pacientes.route("/pacientes", methods=["GET"])
def get_pacientes():
    pacientes = Paciente.query.all()
    pacientes_list = []
    for paciente in pacientes:
        paciente_dict = {
            "tipo_id": paciente.tipo_id,
            "num_paciente_id": paciente.num_paciente_id,
            "nombre_1": paciente.nombre_1,
            "nombre_2": paciente.nombre_2,
            "apellido_1": paciente.apellido_1,
            "apellido_2": paciente.apellido_2,
            "pais": paciente.pais,
            "ciudad": paciente.ciudad,
            "direccion": paciente.direccion,
            "fecha_nacimiento": paciente.fecha_nacimiento.strftime("%Y-%m-%d"),
            "num_telefono": paciente.num_telefono,
            "email": paciente.email,
        }
        pacientes_list.append(paciente_dict)
    return jsonify(pacientes_list)


@pacientes.route("/pacientes/<string:identificador>", methods=["GET"])
def get_paciente(identificador):
    # Primero intenta buscar por num_paciente_id
    paciente = Paciente.query.filter_by(num_paciente_id=identificador).first()

    # Si no se encuentra por num_paciente_id, intenta buscar por tipo_id
    if not paciente:
        paciente = Paciente.query.filter_by(tipo_id=identificador).first()

    if not paciente:
        return jsonify({"message": "Paciente not found"}), 404

    return jsonify(
        {
            "tipo_id": paciente.tipo_id,
            "num_paciente_id": paciente.num_paciente_id,
            "nombre_1": paciente.nombre_1,
            "nombre_2": paciente.nombre_2,
            "apellido_1": paciente.apellido_1,
            "apellido_2": paciente.apellido_2,
            "pais": paciente.pais,
            "ciudad": paciente.ciudad,
            "direccion": paciente.direccion,
            "fecha_nacimiento": paciente.fecha_nacimiento.strftime("%Y-%m-%d"),
            "num_telefono": paciente.num_telefono,
            "email": paciente.email,
        }
    )


# METODO POST


@pacientes.route("/pacientes", methods=["POST"])
def add_paciente():
    data = request.get_json()
    new_paciente = Paciente(
        tipo_id=data["tipo_id"],
        num_paciente_id=data["num_paciente_id"],
        nombre_1=data["nombre_1"],
        nombre_2=data.get("nombre_2"),
        apellido_1=data["apellido_1"],
        apellido_2=data.get("apellido_2"),
        pais=data["pais"],
        ciudad=data["ciudad"],
        direccion=data["direccion"],
        fecha_nacimiento=data["fecha_nacimiento"],
        num_telefono=data["num_telefono"],
        email=data["email"],
    )
    db.session.add(new_paciente)
    db.session.commit()
    return (
        jsonify(
            {
                "tipo_id": new_paciente.tipo_id,
                "num_paciente_id": new_paciente.num_paciente_id,
                "nombre_1": new_paciente.nombre_1,
                "nombre_2": new_paciente.nombre_2,
                "apellido_1": new_paciente.apellido_1,
                "apellido_2": new_paciente.apellido_2,
                "pais": new_paciente.pais,
                "ciudad": new_paciente.ciudad,
                "direccion": new_paciente.direccion,
                "fecha_nacimiento": new_paciente.fecha_nacimiento.strftime("%Y-%m-%d"),
                "num_telefono": new_paciente.num_telefono,
                "email": new_paciente.email,
            }
        ),
        201,
    )


# METODO PUT (UPDATE)


@pacientes.route("/pacientes/<string:num_paciente_id>", methods=["PUT"])
def update_paciente(num_paciente_id):
    data = request.get_json()
    paciente = Paciente.query.filter_by(num_paciente_id=num_paciente_id).first()

    if not paciente:
        return jsonify({"message": "Paciente not found"}), 404

    paciente.tipo_id = data.get("tipo_id", paciente.tipo_id)
    paciente.nombre_1 = data.get("nombre_1", paciente.nombre_1)
    paciente.nombre_2 = data.get("nombre_2", paciente.nombre_2)
    paciente.apellido_1 = data.get("apellido_1", paciente.apellido_1)
    paciente.apellido_2 = data.get("apellido_2", paciente.apellido_2)
    paciente.pais = data.get("pais", paciente.pais)
    paciente.ciudad = data.get("ciudad", paciente.ciudad)
    paciente.direccion = data.get("direccion", paciente.direccion)
    paciente.fecha_nacimiento = data.get("fecha_nacimiento", paciente.fecha_nacimiento)
    paciente.num_telefono = data.get("num_telefono", paciente.num_telefono)
    paciente.email = data.get("email", paciente.email)

    db.session.commit()

    return jsonify(
        {
            "tipo_id": paciente.tipo_id,
            "num_paciente_id": paciente.num_paciente_id,
            "nombre_1": paciente.nombre_1,
            "nombre_2": paciente.nombre_2,
            "apellido_1": paciente.apellido_1,
            "apellido_2": paciente.apellido_2,
            "pais": paciente.pais,
            "ciudad": paciente.ciudad,
            "direccion": paciente.direccion,
            "fecha_nacimiento": paciente.fecha_nacimiento.strftime("%Y-%m-%d"),
            "num_telefono": paciente.num_telefono,
            "email": paciente.email,
        }
    )


# METODO DELETE
@pacientes.route("/pacientes/<string:num_paciente_id>", methods=["DELETE"])
def delete_paciente(num_paciente_id):
    paciente = Paciente.query.filter_by(num_paciente_id=num_paciente_id).first()

    if not paciente:
        return jsonify({"message": "Paciente not found"}), 404

    db.session.delete(paciente)
    db.session.commit()

    return jsonify({"message": "Paciente deleted successfully"})
