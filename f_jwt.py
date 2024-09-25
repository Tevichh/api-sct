from jwt import encode, decode
from jwt import exceptions
from os import getenv
from datetime import datetime, timedelta
from flask import jsonify


def expire_date(days: int):
    return datetime.now() + timedelta(days)

def write_token(data: dict):
    token = encode(payload={**data, "exp": expire_date(2)},
                   key=getenv("SECRET"), algorithm="HS256")
    return token


def validate_token(token, output=False):
    try:
        decoded = decode(token, key=getenv("SECRET"), algorithms=["HS256"])
        if output:
            return {"isTrue": True}
        return None
    except exceptions.DecodeError:
        response = jsonify({"message": "Invalid Token", "isTrue": False})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({"message": "Token Expired", "isTrue": False})
        response.status_code = 401
        return response
    except Exception as e:
        response = jsonify({"message": str(e), "isTrue": False})
        response.status_code = 500
        return response
