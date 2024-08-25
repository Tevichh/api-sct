from flask import Blueprint, jsonify, request
from models.medicos import Medico
from models.users import Users
from utils.db import db

medicos = Blueprint("medicos", __name__)