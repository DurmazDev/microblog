from flask_restful import Resource, request
from app.models.user import UserModel
from app.schemas.user import user_schema
from app.middleware.auth import auth_required


class UserResource(Resource):
    @auth_required
    def get(self):
        user = UserModel.objects.get(id=request.user["id"], deleted_at=None)
        if not user:
            return {"error": "User not found."}, 404
        return user_schema.dump(user)

    @auth_required
    def put(self, id):
        values = request.get_json()
        if request.user["id"] != id:
            return {"error": "You are not authorized for this event."}, 401
        data = user_schema.load(values)
        user = UserModel.objects.get(id=id, deleted_at=None)
        if not user:
            return {"error": "User not found"}, 404

        for key, value in data.items():
            setattr(user, key, value)
        user.save()
        return user_schema.dump(user)

    @auth_required
    def delete(self):
        authenticated_user = UserModel.objects.get(
            id=request.user["id"], deleted_at=None
        )
        if not authenticated_user:
            return {"error": "You are not authorized for this event."}, 401

        # TODO(ahmet): send email for account deletion confirment
        # TODO(ahmet): buradaki email onaylama işlemi yine burada yapılacak
        # query param ile gelen bir token var mı bak, var ise tam silme
        # işlemini gerçekleştir.
        authenticated_user.soft_delete()
        return {
            "message": "An email sent for delete confirmation, please confirm your deletion from your email."
        }, 202
