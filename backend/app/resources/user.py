from flask_restful import Resource, request
from app.models.user import UserModel, UserFollowModel
from app.schemas.user import user_schema, user_follow_schema
from app.middleware.auth import auth_required, check_token
from app.utils import create_audit_log, create_token, decode_token
from bson import ObjectId


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
        create_audit_log(
            5,
            request.remote_addr,
            request.user_agent,
            f"User {user.id} updated.",
        )
        return user_schema.dump(user)

    @auth_required
    def delete(self):
        """
        Soft deletes the authenticated user's account.

        Returns:
            JSON: Message indicating account deletion confirmation email sent.
        """
        verification_token = request.args.get("verificationToken", None, type=str)
        if verification_token:
            try:
                authenticated_user = UserModel.objects(
                    id=request.user["id"], deleted_at=None
                ).get()
            except UserModel.DoesNotExist:
                return {"error": "You are not authorized for this event."}, 401

            if decode_token(verification_token).get("user_id") != request.user["id"]:
                return {"error": "Invalid verification token."}, 400

            authenticated_user.soft_delete()
            return {"message": "Your account has been deleted."}, 200

        # TODO(ahmet): send email for account deletion confirment,
        # send user_id in signed jwt.

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
def get_users_followers_view():
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
def get_users_followings_view():
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
def remove_users_followers_view(id):
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


@auth_required
def setup_2fa_view():
    try:
        user = UserModel.objects(id=request.user["id"], deleted_at=None).get()
    except UserModel.DoesNotExist:
        return {"error": "User not found."}, 404

    if request.method == "DELETE":
        if user.is_2fa_enabled == False:
            return {"error": "2FA is already disabled."}, 400
        user.is_2fa_enabled = False
        del user.secret_token_2fa
        user.save()
        return {"message": "2FA disabled."}, 200

    if user.is_2fa_enabled:
        return {"error": "2FA is already enabled."}, 400
    try:
        secret = user.set_2fa_secret_token()
        uri = user.get_authentication_setup_uri()
        return {"secret": secret, "uri": uri}, 200
    except:
        return {
            "error": "2FA setup failed, administration notified, please try again later."
        }, 500


# @auth_required
def verify_2fa_view(otp):
    token = check_token(request)
    if token != True:
        return {"error": "Unauthorized access."}, 401

    # If 2fa requested, we return a JWT token with only user id in login view,
    # so, if we have email field in JWT, user was logged in.
    if "email" in request.user.keys():
        return {"error": "Already logged in."}, 400

    try:
        user = UserModel.objects(id=request.user["id"], deleted_at=None).get()
    except UserModel.DoesNotExist:
        return {"error": "User not found."}, 404

    if not user.is_otp_valid(otp):
        return {"error": "Invalid OTP."}, 400

    if not user.is_2fa_enabled:
        user.is_2fa_enabled = True
        user.save()

    user_data = user_schema.dump(user)
    return {
        "message": "2FA verification successfull.",
        "token": create_token(user_data),
        "user": user_data,
    }, 200
