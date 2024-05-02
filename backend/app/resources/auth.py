from flask_restful import request, current_app
from app.models.user import UserModel
from app.schemas.user import user_schema
from app.utils import create_token, create_audit_log
from app.middleware.auth import auth_required
from bcrypt import checkpw, hashpw, gensalt


@auth_required
def RefreshView():
    """
    Refreshes an authentication token.

    Endpoint:
        POST /auth/refresh

    Returns:
        JSON: Authentication token and user data on successful refresh, or error message on authentication failure.
    """
    current_app.config["logout_blocklist"].block_user(request.user["id"], request.token)
    return {
        "message": "Successfully refreshed token.",
        "token": create_token(request.user),
        "user": request.user,
    }, 200


@auth_required
def LogOutView():
    """
    Logs out a user by adding the user ID to the blacklist.

    Endpoint:
        POST /auth/logout

    Returns:
        JSON: Success message on successful logout.
    """
    current_app.config["logout_blocklist"].block_user(request.user["id"], request.token)
    # current_app.config["jwt_redis_blocklist"].set(
    #     request.user["id"], request.token, ex=current_app.config["REDIS_TOKEN_EXPIRES"]
    # )
    return {"message": "Successfully logged out."}, 202


def LoginView():
    """
    Logs in a user and returns an authentication token.

    Endpoint:
        POST /auth/login

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

    try:
        user = UserModel.objects(email=values["email"], deleted_at=None).get()
    except UserModel.DoesNotExist:
        return {"error": "Wrong email or password."}, 401

    user_data = user_schema.dump(user)

    if checkpw(values["password"].encode("utf-8"), user["password"].encode("utf-8")):
        if user.is_2fa_enabled:
            create_audit_log(
                1, request.remote_addr, request.user_agent, f"User {user.id} tries login, 2fa requested."
            )
            return {
                "message": "2FA is enabled, redirect to 2FA verification.",
                "token": create_token({"id": str(user.id)}),
            }, 302
        create_audit_log(
            1, request.remote_addr, request.user_agent, f"User {user.id} logged in."
        )
        return {
            "message": "Successfully logged in.",
            "token": create_token(user_data),
            "user": user_data,
        }, 200

    create_audit_log(
        2, request.remote_addr, request.user_agent, "Authentication failure."
    )
    return {"error": "Wrong email or password."}, 401


def RegisterView():
    """
    Registers a new user and returns an authentication token.

    Endpoint:
        POST /auth/register

    Returns:
        JSON: Authentication token and user data on successful registration, or error message if user already exists.
    """
    values = request.get_json()
    errors = user_schema.validate(values)
    if errors:
        return {"error": "Unallowed attribute."}, 400

    # WARN(ahmet): maybe this should be a custom validator?
    try:
        user = UserModel.objects(email=values["email"], deleted_at=None).get()
        if user:
            return {"error": "User with this e-mail already exists."}, 409
    except UserModel.DoesNotExist:
        pass

    user = UserModel(
        name=values["name"],
        email=values["email"],
        password=hashpw(values["password"].encode("utf-8"), gensalt(rounds=12)),
    ).save()

    create_audit_log(
        1, request.remote_addr, request.user_agent, f"User {user.id} created."
    )

    user_data = user_schema.dump(user)
    return {
        "message": "User created successfully.",
        "token": create_token(user_data),
        "user": user_data,
    }, 201
