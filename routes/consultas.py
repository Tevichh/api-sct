from flask import Blueprint, jsonify, request
from models.consulta import Consulta
from utils.db import db
from f_jwt import validate_token
from src.prueba import examenConsulta
import os

consulta = Blueprint("consultas", __name__)


#@consulta.before_request  ####
def validar_token():
    if request.method != "GET":
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


@consulta.route("/consultas")
def get_consultas():
    consultas = Consulta.query.all()
    consultas_list = []

    for consulta in consultas:
        consulta_dict = {
            "id": consulta.id,
            "identificacion": consulta.identificacion,
            "nombreCompleto": consulta.nombreCompleto,
            "fecha": consulta.fecha,
            "muestraUrl": consulta.muestraUrl,
            "resultado": consulta.resultado,
            "observaciones": consulta.observaciones,
            "medico": consulta.medico,
        }
        consultas_list.append(consulta_dict)
    return jsonify(consultas_list)


@consulta.route("/consultas/<string:identificador>")
def get_consulta(identificador):
    consultas = Consulta.query.filter_by(identificacion=identificador)
    consultas_list = []

    for consulta in consultas:
        consulta_dict = {
            "id": consulta.id,
            "identificacion": consulta.identificacion,
            "nombreCompleto": consulta.nombreCompleto,
            "fecha": consulta.fecha,
            "muestraUrl": consulta.muestraUrl,
            "resultado": consulta.resultado,
            "observaciones": consulta.observaciones,
            "medico": consulta.medico,
        }
        consultas_list.append(consulta_dict)
    return jsonify(consultas_list)


# METODO POST


@consulta.route("/consultas", methods=["POST"])
def add_consulta():
    data = request.get_json()

    new_consulta = Consulta(
        identificacion=data["identificacion"],
        nombreCompleto=data["nombreCompleto"],
        fecha=data["fecha"],
        muestraUrl=data["muestraUrl"],
        resultado="",
        observaciones=data["observaciones"],
        medico=data["medico"],
    )

    new_consulta.resultado = examenConsulta(new_consulta.muestraUrl)

    db.session.add(new_consulta)
    db.session.commit()

    return (
        jsonify(
            {
                "identificacion": new_consulta.identificacion,
                "nombreCompleto": new_consulta.nombreCompleto,
                "fecha": new_consulta.fecha,
                "muestraUrl": new_consulta.muestraUrl,
                "resultado": new_consulta.resultado,
                "observaciones": new_consulta.observaciones,
                "medico": new_consulta.medico,
            }
        ),
        201,
    )


@consulta.route("/consultas/muestra", methods=["POST"])
def method_name():
    if "muestra" not in request.files:
        return "No se ha seleccionado ninguna imagen", 400

    file = request.files["muestra"]

    if file.filename == "":
        return "No se ha seleccionado ninguna imagen", 400

    rutaImagenes = "src/muestrasPacientes/examenes"
    path = os.path.join(rutaImagenes, file.filename)

    file.save(path)

    return f"Imagen subida con éxito: {file.filename}"

