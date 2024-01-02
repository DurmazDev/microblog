from flask import request
from flask_restful import current_app
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
            logout_query = current_app.config["jwt_redis_blocklist"].get(
                decoded_token["id"]
            )
            if logout_query is not None and logout_query == token:
                return {"error": "Invalid token"}, 401

            request.user = decoded_token
            request.token = token
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}, 401
        except KeyError:
            return {"error": "Invalid token"}, 401

        return func(*args, **kwargs)

    return wrapper
