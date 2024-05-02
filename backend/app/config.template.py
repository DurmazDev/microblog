APP_NAME = "Microblog"
DEBUG = False
PORT = 8000
HOST = "0.0.0.0"
REDIS_SETTINGS = {"host": "redis-service", "port": 6379, "db": 0}
REDIS_URI = (
    "redis://"
    + REDIS_SETTINGS["host"]
    + ":"
    + str(REDIS_SETTINGS["port"])
    + "/"
    + str(REDIS_SETTINGS["db"])
)
MONGODB_SETTINGS = {"host": "mongodb://mongo-service:27017/microblog"}
REDIS_SYNC_INTERVAL = 60  # In minutes
MAX_BLOCKED_USER = 10000
DOMAIN_ROOT = HOST + ":" + str(PORT)
FRONTEND_ROOT = "microblog.local:4173"
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
    "ul",
    "li",
    "ol",
    "strong",
    "h1",
    "h2",
    "h3",
    "pre",
]
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "rel", "target"],  # INFO(ahmet): css can be enabled
    "abbr": ["title"],
    "acronym": ["title"],
}
