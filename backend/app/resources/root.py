from flask_restful import Resource


class RootResource(Resource):
    def get(self):
        return {"message": "Hello world!"}, 200
