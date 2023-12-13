from flask_restful import request
from app.models.user import UserModel
from app.schemas.user import user_schema
from bcrypt import checkpw, hashpw, gensalt
from app.utils import create_token


def LoginView():
    """
    Logs in a user and returns an authentication token.

    Endpoint:
        POST /login

        Body:
        {
            "email": "string",
            "password": "string"
        }

    Returns:
        JSON: Authentication token and user data on successful login, or error message on authentication failure.
    """
    values = request.get_json()
    errors = user_schema.validate(values)
    if errors:
        return {"error": "Unallowed attribute."}, 400

    user = UserModel.objects(email=values["email"], deleted_at=None).first()
    if not user:
        return {"error": "User not found."}, 404

    user_data = user_schema.dump(user)

    if checkpw(values["password"].encode("utf-8"), user["password"].encode("utf-8")):
        return {
            "message": "Successfully logged in.",
            "token": create_token(user_data),
            "user": user_data,
        }, 200
    return {"error": "Wrong email or password."}, 401


def RegisterView():
    """
    Registers a new user and returns an authentication token.

    Endpoint:
        POST /register

    Returns:
        JSON: Authentication token and user data on successful registration, or error message if user already exists.
    """
    values = request.get_json()
    errors = user_schema.validate(values)
    if errors:
        return {"error": "Unallowed attribute."}, 400

    user = UserModel.objects(email=values["email"], deleted_at=None).first()
    if user:
        return {"error": "User with this e-mail already exists."}, 409

    user = UserModel(
        name=values["name"],
        email=values["email"],
        password=hashpw(values["password"].encode("utf-8"), gensalt(rounds=12)),
    ).save()

    user_data = user_schema.dump(user)
    return {
        "message": "User created successfully.",
        "token": create_token(user_data),
        "user": user_data,
    }, 201
