class Config:
    DEBUG = True
    PORT = 8000
    MONGODB_SETTINGS = {"host": "mongodb://172.17.0.2:27017/microblog"}


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
DOMAIN_ROOT = "127.0.0.1:" + str(Config.PORT)
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
