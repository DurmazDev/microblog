from flask import request
from functools import wraps
from app.config import SECRET_KEY, JWT_ALGORITHM
from bson import ObjectId
import jwt


def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return {"error": "Token is missing"}, 401
        token = token.split(" ")[1]

        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
            if not ObjectId.is_valid(decoded_token["id"]):
                return {"error": "Invalid token"}, 401
            request.user = decoded_token
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}, 401
        except KeyError:
            return {"error": "Invalid token"}, 401

        return func(*args, **kwargs)

    return wrapper
