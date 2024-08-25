from flask import Blueprint, jsonify, request
from models.paciente import Paciente
from utils.db import db

pacientes = Blueprint("consultas", __name__)