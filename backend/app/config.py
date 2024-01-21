DEBUG = True
PORT = 8000
HOST = "0.0.0.0"
REDIS_SETTINGS = {"host": "127.0.0.1", "port": 6379, "db": 0}
REDIS_URI = (
    "redis://"
    + REDIS_SETTINGS["host"]
    + ":"
    + str(REDIS_SETTINGS["port"])
    + "/"
    + str(REDIS_SETTINGS["db"])
)
MONGODB_SETTINGS = {"host": "mongodb://127.0.0.1:27017/microblog"}
REDIS_SYNC_INTERVAL = 60  # In minutes
MAX_BLOCKED_USER = 10000
DOMAIN_ROOT = HOST + ":" + str(PORT)
FRONTEND_ROOT = "localhost:5173"
SECRET_KEY = "usmanim_nereye_gidersin_youtu.be/0ZPg9GwExFg"
JWT_ALGORITHM = "HS256"
ALLOWED_TAGS = [
    "p",
    "br",
    "a",
    "abbr",
    "acronym",
    "b",
    "blockquote",
    "code",
    "em",
    "i",
    "li",
    "ol",
    "strong",
    "ul",
]
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"],  # INFO(ahmet): css can be enabled
    "abbr": ["title"],
    "acronym": ["title"],
}
LOGGER_NAME = "flask"
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname}: {asctime} - {module} - Process: {process:d} - Thread: {thread:d} - {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname}: {asctime} - {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "formatter": "verbose",
            "class": "logging.FileHandler",
            "filename": "app/log/flask-debug.log",
        },
    },
    "loggers": {
        LOGGER_NAME: {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
