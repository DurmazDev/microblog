from flask import request
from flask_restful import current_app
from functools import wraps
from app.utils import decode_token
from bson import ObjectId
import jwt


def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return {"error": "Token is missing."}, 401
        token = token.split(" ")[-1]

        try:
            decoded_token = decode_token(token)
            if not ObjectId.is_valid(decoded_token["id"]):
                return {"error": "Invalid token."}, 401
            logout_query = current_app.config["logout_blocklist"].check_token(
                decoded_token["id"], token
            )
            if logout_query:
                return {"error": "Invalid token."}, 401

            request.user = decoded_token
            request.token = token
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired."}, 401
        except jwt.PyJWTError:
            return {"error": "Invalid token."}, 401

        return func(*args, **kwargs)

    return wrapper
