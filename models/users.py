from utils.db import db


class Users(db.Model):
    __tablename__ = "User"

    id = db.Column(
        db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True
    )
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    rol = db.Column(db.String(50), nullable=False)
