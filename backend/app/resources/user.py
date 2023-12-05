from flask_restful import Resource, request
from bson import ObjectId
from app.models.user import UserModel
from app.schemas.user import user_schema
from app.middleware.auth import auth_required


class UserResource(Resource):
    @auth_required
    def get(self):
        user = UserModel.get_by_id(user_id=request.user["id"])
        if not user:
            return {"error": "User not found."}, 404
        return user_schema.dump(user)

    @auth_required
    def put(self, id):
        values = request.get_json()
        if request.user["id"] != id:
            return {"error": "You are not authorized for this event."}, 401
        data = user_schema.load(values)
        user = UserModel.get_by_id(user_id=id)
        if not user:
            return {"error": "User not found"}, 404
        updated_user = UserModel.update(user_id=id, update_values=data)
        if updated_user:
            return user_schema.dump(updated_user)

        return {"error": "User not found."}, 404

    @auth_required
    def delete(self, id):
        authenticated_user = UserModel.get_by_id(user_id=request.user["id"])
        if not authenticated_user or authenticated_user.id != ObjectId(id):
            return {"error": "You are not authorized for this event."}, 401
        user = UserModel.get_by_id(user_id=id)
        if not user:
            return {"error": "User not found"}, 404

        # TODO(ahmet): send email for account deletion confirment
        # TODO(ahmet): buradaki email onaylama işlemi yine burada yapılacak
        # query param ile gelen bir token var mı bak, var ise tam silme
        # işlemini gerçekleştir.
        return {
            "message": "An email sent for delete confirmation, please confirm your deletion from your email."
        }, 202
