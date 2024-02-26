from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from mongoengine import (
    NotUniqueError,
    ValidationError as ME_ValidationError,
    DoesNotExist,
)
from marshmallow import ValidationError as MMW_ValidationError
from app.config import REDIS_SYNC_INTERVAL, REDIS_SETTINGS, REDIS_URI, MONGODB_SETTINGS
from app.utils import LogOutBlockList
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from app.database import connect_redis, connect_mongodb
import logging

from app.resources.root import RootResource
from app.resources.user import UserResource
from app.resources.post import PostResource, ShowPostResource
from app.resources.feed import FeedResource
from app.resources.vote import VoteResource
from app.resources.comment import CommentResource
from app.resources.auth import LoginView, RegisterView, LogOutView, RefreshView


def create_app(
    mongodb_uri=MONGODB_SETTINGS["host"],
    REDIS_SETTINGS=REDIS_SETTINGS,
    redis_client=None,
    **kwargs,
):
    logging.basicConfig(
        filename="app/log/flask-error.log", level=logging.ERROR, filemode="a+"
    )
    app = Flask(__name__)
    api = Api(app)

    CORS(app=app)

    app.config["REDIS_TOKEN_EXPIRES"] = timedelta(days=1)
    app.config["BLOCKED_USERS"] = []

    if kwargs.get("TESTING") == True and redis_client != None:
        app.config["jwt_redis_blocklist"] = redis_client
    else:
        app.config["jwt_redis_blocklist"] = connect_redis(
            redis_host=REDIS_SETTINGS["host"],
            redis_port=REDIS_SETTINGS["port"],
            redis_db=REDIS_SETTINGS["db"],
        )

    app.config["logout_blocklist"] = LogOutBlockList(app.config["BLOCKED_USERS"])

    scheduler = BackgroundScheduler()
    # Scheduler runs sync_redis twice when use_reload=True or DEBUG=True.
    scheduler.add_job(
        app.config["logout_blocklist"].sync_redis,
        "interval",
        minutes=REDIS_SYNC_INTERVAL,
        args=[app.config["jwt_redis_blocklist"]],
    )
    scheduler.start()

    connect_mongodb(mongodb_uri, **kwargs)

    @app.errorhandler(MMW_ValidationError)  # Marshmallow Validation Error
    def handle_validation_error(error):
        app.logger.error(error)
        return {"error": "Validation error"}, 400

    @app.errorhandler(ME_ValidationError)  # MongoEngine Validation Error
    def handle_validation_error(error):
        app.logger.error(error)
        return {"error": "Unsupported ID value."}, 400

    @app.errorhandler(NotUniqueError)
    def handle_notunique_error(error):
        app.logger.error(error)
        return {"error": "Bad request."}, 400

    @app.errorhandler(DoesNotExist)
    def handle_doesnotexists_error(error):
        app.logger.error(error)
        return {"error": "Not found."}, 404

    @app.errorhandler(KeyError)
    def handle_key_error(error):
        app.logger.error(error)
        return {"error": "An error occurred."}, 500

    @app.errorhandler(404)
    def handle_not_found_error(error):
        app.logger.error(error)
        return {"error": "Not found."}, 404

    @app.errorhandler(Exception)
    def handle_other_errors(error):
        app.logger.error(error)
        return {"error": "An error occurred."}, 500

    if kwargs.get("TESTING") == False:
        Limiter(
            get_remote_address,
            app=app,
            default_limits=["4000 per hour"],
            storage_uri=REDIS_URI,
            storage_options={"socket_connect_timeout": 30},
            strategy="moving-window",
        )

    api.add_resource(RootResource, "/")
    api.add_resource(UserResource, "/user", "/user/<string:id>")
    api.add_resource(ShowPostResource, "/post/<string:id>")
    api.add_resource(PostResource, "/post", "/post/<string:id>")
    api.add_resource(CommentResource, "/comment", "/comment/<string:id>")
    api.add_resource(VoteResource, "/vote")
    api.add_resource(FeedResource, "/feed")
    app.add_url_rule("/auth/login", "login", LoginView, methods=["POST"])
    app.add_url_rule("/auth/register", "register", RegisterView, methods=["POST"])
    app.add_url_rule("/auth/logout", "logout", LogOutView, methods=["DELETE"])
    app.add_url_rule("/auth/refresh", "refresh", RefreshView, methods=["POST"])

    return app
