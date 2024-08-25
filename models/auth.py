from utils.db import db


class Auth(db.Model):
    __tablename__ = "Auth"

    id = db.Column(
        db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True
    )
    token = db.Column(db.String(50), unique=True, nullable=False)
  