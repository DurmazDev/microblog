from flask import request
from flask_restful import current_app
from functools import wraps
from app.utils import decode_token, create_audit_log
from bson import ObjectId
import jwt


def check_token(req):
    token = req.headers.get("Authorization")
    if not token:
        create_audit_log(
            0,
            req.remote_addr,
            req.user_agent,
            "Token is missing. Unauthorized access tried.",
        )
        return {"error": "Token is missing."}, 401
    token = token.split(" ")[-1]
    try:
        decoded_token = decode_token(token)
        if not ObjectId.is_valid(decoded_token["id"]):
            create_audit_log(
                0,
                req.remote_addr,
                req.user_agent,
                "Invalid token.",
            )
            return False
        logout_query = current_app.config["logout_blocklist"].check_token(
            decoded_token["id"], token
        )
        if logout_query:
            create_audit_log(
                0,
                req.remote_addr,
                req.user_agent,
                "Invalid token.",
            )
            return False

        req.user = decoded_token
        req.token = token
        return True
    except jwt.ExpiredSignatureError:
        create_audit_log(
            0,
            req.remote_addr,
            req.user_agent,
            "Token has expired.",
        )
        return False
    except jwt.PyJWTError:
        create_audit_log(0, req.remote_addr, req.user_agent, "Invalid token.")
        return False


def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            create_audit_log(
                0,
                request.remote_addr,
                request.user_agent,
                "Token is missing. Unauthorized access tried.",
            )
            return {"error": "Token is missing."}, 401
        token = token.split(" ")[-1]

        try:
            decoded_token = decode_token(token)
            if not ObjectId.is_valid(decoded_token["id"]):
                create_audit_log(
                    0,
                    request.remote_addr,
                    request.user_agent,
                    "Invalid token.",
                )
                return {"error": "Invalid token."}, 401
            logout_query = current_app.config["logout_blocklist"].check_token(
                decoded_token["id"], token
            )
            if logout_query:
                create_audit_log(
                    0,
                    request.remote_addr,
                    request.user_agent,
                    "Invalid token.",
                )
                return {"error": "Invalid token."}, 401

            request.user = decoded_token
            request.token = token
        except jwt.ExpiredSignatureError:
            create_audit_log(
                0,
                request.remote_addr,
                request.user_agent,
                "Token has expired.",
            )
            return {"error": "Token has expired."}, 401
        except jwt.PyJWTError:
            create_audit_log(
                0,
                request.remote_addr,
                request.user_agent,
                "Invalid token.",
            )
            return {"error": "Invalid token."}, 401

        return func(*args, **kwargs)

    return wrapper
