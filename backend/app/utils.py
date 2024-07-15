from flask_restful import current_app
from app.config import SECRET_KEY, MAX_BLOCKED_USER, JWT_ALGORITHM
from datetime import datetime, timedelta
from app.models.audit import AuditModel
from io import BytesIO
from base64 import b64encode
import logging
import math
import jwt


class LogOutBlockList:
    """
    A class to manage blocked users.

    Attributes
    ----------
    blocked_users: List[User]
        List of blocked users.

    Methods
    -------
    block_user(user_id: str, token: str)
        Adds a user to the blocked users list.
    sync_redis()
        Syncs blocked users to Redis.
    check_token(user_id: str, token: str)
        Checks if a user is blocked.
    """

    class User:
        def __init__(self, id: str, token: str):
            self.id = id
            self.token = token
            self.expire_at = current_app.config["REDIS_TOKEN_EXPIRES"]
            self.created_at = datetime.utcnow()

    def __init__(self, blocked_users: list = []):
        self.blocked_users = blocked_users

    def block_user(self, user_id: str, token: str):
        # Check blocked_users if user is already blocked
        blocked_user = list(
            filter(lambda blocked_user: blocked_user.id == user_id, self.blocked_users)
        )
        if len(blocked_user) == 0:
            self.blocked_users.append(self.User(id=user_id, token=token))
        else:
            blocked_user[0].token = token

    # This method called every hour.
    def sync_redis(self, redis_connection):
        for user in self.blocked_users:
            if datetime.utcnow() > user.expire_at + user.created_at:
                self.blocked_users.remove(user)
            else:
                redis_connection.set(user.id, user.token)

        # Set max number to avoid memory problems.
        if len(self.blocked_users) == MAX_BLOCKED_USER:
            self.blocked_users = []

    def check_token(self, user_id, token):
        """
        Checks if the provided token is valid for the given user ID.

        Parameters:
        - user_id (ObjectID): The ObjectID of the user.
        - token (str): The token to be checked.

        Returns:
        - bool: True if the token is valid, False otherwise.
        """
        blocked_user = list(
            filter(lambda blocked_user: blocked_user.id == user_id, self.blocked_users)
        )
        if len(blocked_user) == 0:
            logout_query = current_app.config["jwt_redis_blocklist"].get(user_id)
            if logout_query is not None and logout_query == token:
                return True
            return False
        else:
            return blocked_user[0].token == token


def create_token(data: object):
    """
    Signs data with JWT.

    Parameters
    ---------
    data: Object

    Returns
    ---------
    string
        JWT signed token.
    """
    return jwt.encode(
        {"exp": datetime.utcnow() + timedelta(days=1), **data},
        SECRET_KEY,
        algorithm="HS256",
    )


def decode_token(token: str):
    """
    Decodes JWT token.

    Parameters
    ---------
    token: str

    Returns
    ---------
    dict
        Decoded token.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])


def paginate_query(query, page: int, limit: int, schema, sort: [str] = []):
    """
    Paginates a query and returns results along with pagination information.

    Parameters
    ----------
    query: QuerySet
        The query to paginate.
    page: int
        Current page number.
    limit: int
        Number of items per page.
    schema: Schema
        Schematic of the query model.
    sort: List[String] -> Example: ["-created_at", "vote"]


    Returns
    -------
    dict
        Paginated results with pagination information.
    """
    page = 1 if page < 1 else page
    limit = 50 if limit < 1 else limit
    # WARN(ahmet): If page greater than total_page we should not run the query
    offset = (page - 1) * limit
    results = query.skip(offset).limit(limit)

    if sort:
        results = results.order_by(*sort)

    result_count = query.count()

    if result_count == 0 or len(results) == 0:
        return {"error": "No results found."}, 404

    results = schema.dump(results, many=True)
    total_pages = math.ceil(result_count / limit)

    return {
        "results": results,
        "pagination": {
            "current_page": page,
            "next_page": None if page == total_pages else page + 1,
            "prev_page": None if page == 1 else page - 1,
            "total_count": result_count,
            "total_pages": total_pages,
        },
    }, 200


def create_audit_log(
    event_id: int = None,
    request_ip: str = None,
    request_user_agent: str = None,
    description: str = None,
):
    """
    This function creates an audit log.

    Parameters
    ----------
    event_id: int
        The event ID.
    request_ip: str
        The IP address of the request.
    request_user_agent: str
        The user agent of the request.
    description: str
        The description of the event.

    Returns
    -------
    None
    """
    try:
        AuditModel.objects.create(
            event_id=event_id,
            description=str(description),
            request_ip=str(request_ip),
            request_user_agent=str(request_user_agent),
        )
    except:
        # Dunno this is the best way, but we should log the error.
        logging.error(
            f"Audit log creation failed. Audit log details: {event_id}, {description}, {request_ip}, {request_user_agent}"
        )
        pass
