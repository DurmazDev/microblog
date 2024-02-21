import redis
from mongoengine import connect


def connect_mongodb(mongodb_uri, **kwargs):
    connect(host=mongodb_uri, **kwargs)


def connect_redis(redis_host, redis_port, redis_db, **kwargs):
    return redis.StrictRedis(
        host=redis_host, port=redis_port, db=redis_db, decode_responses=True, **kwargs
    )
