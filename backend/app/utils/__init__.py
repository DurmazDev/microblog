from app.config import SECRET_KEY
import jwt


def create_token(data: object):
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")
