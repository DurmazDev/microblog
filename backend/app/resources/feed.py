from flask_restful import Resource


class FeedResource(Resource):
    def get(self):
        return {"null": None}, 200
