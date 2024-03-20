from flask_restful import Resource, request
from app.models.user import UserModel, UserFollowModel
from app.schemas.user import user_schema, user_follow_schema
from app.middleware.auth import auth_required
from bson import ObjectId
import json


class UserResource(Resource):
    """
    Endpoint:
        GET /user
        PUT /user/<id>
        DELETE /user
    """

    @auth_required
    def get(self):
        """
        Retrieves the profile information of the authenticated user.

        Returns:
            JSON: User profile details.
        """
        try:
            user = UserModel.objects(id=request.user["id"], deleted_at=None).get()
        except UserModel.DoesNotExist:
            return {"error": "User not found."}, 404
        return user_schema.dump(user)

    @auth_required
    def put(self, id):
        """
        Updates the profile information of the authenticated user.

        Parameters:
            id (str): User ID

        Body:
            {
                "name": "string",
                "email": "string",
                "password": "string"
            }

        Returns:
            JSON: Updated user profile details.
        """
        values = request.get_json()
        if request.user["id"] != id:
            return {"error": "You are not authorized for this event."}, 401
        data = user_schema.load(values)
        try:
            user = UserModel.objects(id=id, deleted_at=None).get()
        except UserModel.DoesNotExist:
            return {"error": "User not found"}, 404

        for key, value in data.items():
            setattr(user, key, value)
        user.save()
        return user_schema.dump(user)

    @auth_required
    def delete(self):
        """
        Soft deletes the authenticated user's account.

        Returns:
            JSON: Message indicating account deletion confirmation email sent.
        """
        try:
            authenticated_user = UserModel.objects(
                id=request.user["id"], deleted_at=None
            ).get()
        except UserModel.DoesNotExist:
            return {"error": "You are not authorized for this event."}, 401

        # TODO(ahmet): send email for account deletion confirment
        # TODO(ahmet): buradaki email onaylama işlemi yine burada yapılacak
        # query param ile gelen bir token var mı bak, var ise tam silme
        # işlemini gerçekleştir.
        authenticated_user.soft_delete()
        return {
            "message": "An email sent for delete confirmation, please confirm your deletion from your email."
        }, 202


class UserFollowResource(Resource):
    @auth_required
    def post(self, id):
        if request.user["id"] == id:
            return {"error": "You cannot follow yourself."}, 400
        try:
            user = UserModel.objects(id=id, deleted_at=None).get()
        except UserModel.DoesNotExist:
            return {"error": "User not found."}, 404

        try:
            UserFollowModel.objects(
                follower_id=request.user["id"], followee_id=id, deleted_at=None
            ).get()
            return {"error": "You already follow this user."}, 409
        except UserFollowModel.DoesNotExist:
            pass

        # check soft deleted
        try:
            user_follow = UserFollowModel.objects(
                follower_id=request.user["id"], followee_id=id, deleted_at__ne=None
            ).get()
            if user_follow != None:
                user_follow.deleted_at = None
                user_follow.save()
                return {"message": "You are now following this user."}, 201
        except UserFollowModel.DoesNotExist:
            pass

        user_follow = UserFollowModel(
            follower_id=request.user["id"], followee_id=id
        ).save()
        return {"message": "You are now following this user."}, 201

    @auth_required
    def delete(self, id):
        if request.user["id"] == id:
            return {"error": "You cannot unfollow yourself."}, 400
        try:
            user_follow = UserFollowModel.objects(
                follower_id=request.user["id"], followee_id=id, deleted_at=None
            ).get()
        except UserFollowModel.DoesNotExist:
            return {"error": "You are not following this user."}, 404

        user_follow.soft_delete()
        return {"message": "You are not following this user anymore."}, 202


@auth_required
def getUsersFollowersView():
    try:
        user_followers = UserFollowModel.objects(
            followee_id=request.user["id"], deleted_at=None
        ).all()
        if len(user_followers) == 0:
            return {"error": "Nobody following you."}, 404
    except UserFollowModel.DoesNotExist:
        return {"error": "Nobody following you."}, 404

    user_ids = [data["follower_id"] for data in user_followers]
    user_data = UserModel.objects(id__in=user_ids).only("id", "name")
    user_data_map = {user.id: user.name for user in user_data}
    followers = []

    for data in user_followers:
        follower_id = data["follower_id"]
        user_name = user_data_map.get(ObjectId(follower_id), "Deleted user")
        followers.append({"id": follower_id, "name": user_name})

    return user_follow_schema.dump(followers, many=True)


@auth_required
def getUsersFollowingsView():
    try:
        user_followings = UserFollowModel.objects(
            follower_id=request.user["id"], deleted_at=None
        ).all()
        if len(user_followings) == 0:
            return {"error": "You are not following anyone."}, 404
    except UserFollowModel.DoesNotExist:
        return {"error": "You are not following anyone."}, 404

    user_ids = [data["followee_id"] for data in user_followings]
    user_data = UserModel.objects(id__in=user_ids).only("id", "name")
    user_data_map = {user.id: user.name for user in user_data}
    followings = []

    for data in user_followings:
        followee_id = data["followee_id"]
        user_name = user_data_map.get(ObjectId(followee_id), "Deleted user")
        followings.append({"id": followee_id, "name": user_name})

    return user_follow_schema.dump(followings, many=True)


@auth_required
def removeUsersFollowersView(id):
    if request.user["id"] == id:
        return {"error": "You cannot unfollow yourself."}, 400
    try:
        user_follow = UserFollowModel.objects(
            followee_id=request.user["id"], follower_id=id, deleted_at=None
        ).get()
    except UserFollowModel.DoesNotExist:
        return {"error": "User are not following you."}, 404

    user_follow.soft_delete()
    return {"message": "User are not following you anymore."}, 202
