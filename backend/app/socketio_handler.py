from app.utils import decode_token
from app.middleware.auth import auth_required
from flask_restful import request
from flask_socketio import emit, rooms, join_room, leave_room
from uuid import uuid4


def handle_socketio_requests(socketio, app):
    """
    This function is used to handle the socketio requests.

    Args:
        socketio (SocketIO): The socketio object.
        app (Flask): The flask app object.

    Returns:
        None
    """
    socket_active_users = []

    def set_notification_data(notification_event, user_name, other_data=None):
        """
        This function is used to set the notification data.

        Args:
            notification_event (int): The event type of the notification.
            user_name (str): The name of the user to notify.
            other_data (dict): The additional data to send to the client.

        Returns:
            dict: The notification data.

        Event Types:
            0: Follow
            Args:
                user_id: The user id of the user to notify.

            1: Unfollow
            Args:
                user_id: The user id of the user to notify.

            2: Private Chat Request
            Args:
                user_id: The user id of the user to notify.
                additional_data: The additional_data object includes room_id.

            3: Voted Your Post
            Args:
                user_id: The user id of the user to notify.

            4: Removed you from their followers list
            Args:
                user_id: The user id of the user to notify.

            5: Commented on your post
            Args:
                user_id: The user id of the user to notify.
                additional_data: The additional_data object includes post_id.
        """
        notification_data = {
            "notification_id": uuid4().hex,
        }

        if notification_event == 0:
            notification_data["message"] = f"{user_name} has followed you."
        elif notification_event == 1:
            notification_data["message"] = f"{user_name} has unfollowed you."
        elif notification_event == 2:
            notification_data["message"] = (
                f"{user_name} has sent you a private chat request."
            )
            if other_data != None:
                notification_data["room_id"] = other_data.get("room_id")
        elif notification_event == 3:
            notification_data["message"] = f"{user_name} has voted your post."
        elif notification_event == 4:
            notification_data["message"] = (
                f"{user_name} has removed you from his/her followers list."
            )
        elif notification_event == 5:
            notification_data["message"] = f"{user_name} has commented on your post."
            if other_data != None:
                notification_data["post_id"] = other_data.get("post_id")

        if notification_data.get("message") == None:
            return None
        return notification_data

    def join_user(user_id, name):
        """
        This function is used to add the user to the active users list.

        Args:
            user_id (str): The user id of the user.
            name (str): The name of the user.

        Returns:
            None
        """
        user_ids = [user.get("user_id") for user in socket_active_users]
        if user_id not in user_ids:
            socket_active_users.append(
                {"name": name, "user_id": user_id, "sid": request.sid}
            )
        else:
            user_index = user_ids.index(user_id)
            socket_active_users[user_index]["sid"] = request.sid

    def leave_user(user_id=None, sid=None):
        """
        This function is used to remove the user from the active users list.

        Args:
            user_id (str): The user id of the user.
            sid (str): The session id of the user.

        Returns:
            None
        """
        if user_id != None:
            user_ids = [user.get("user_id") for user in socket_active_users]
        elif sid != None:
            user_ids = [user.get("sid") for user in socket_active_users]
        else:
            return
        if user_id in user_ids:
            user_index = user_ids.index(user_id)
            socket_active_users.pop(user_index)

    @socketio.on("active_users")
    @auth_required
    def get_active_users(data):
        emit("active_users", {"users": socket_active_users})

    @socketio.on("message")
    @auth_required
    def handle_message(data):
        user = request.user["name"]
        user_id = request.user["id"]

        room = data.get("room")
        message = data.get("message")
        if room == None or message == None:
            return
        if room in rooms():
            emit(
                "message",
                {"name": user, "user_id": user_id, "message": message},
                to=room,
            )

    @socketio.on("join")
    @auth_required
    def on_join(data):
        user = request.user["name"]
        user_id = request.user["id"]

        join_user(user_id, user)
        room = data.get("room")

        join_room(room)
        emit("active_users", socket_active_users, to=room)
        emit("join", {"name": user, "user_id": user_id}, to=room)

    @socketio.on("private_chat_request")
    @auth_required
    def on_private_chat_request(data):
        """
        This function is used to send private chat requests.

        Args:
            data (dict): The data sent by the client.

        Returns:
            None
        """
        user = request.user["name"]
        user_id = request.user["id"]

        private_room_id = data.get("private_room_id")
        invited_user_id = data.get("invited_user_id")
        room = data.get("room")
        if room == None:
            return

        # Get sid from the active users list.
        invited_user_sid = [
            user.get("sid")
            for user in socket_active_users
            if user.get("user_id") == invited_user_id
        ]
        if len(invited_user_sid) == 0:
            return
        invited_user_sid = invited_user_sid[0]
        notification_data = set_notification_data(2, user, {"room_id": private_room_id})
        emit(
            "notification",
            {**notification_data},
            to=invited_user_sid,
        )
        emit(
            "private_chat_request",
            {
                "name": user,
                "user_id": user_id,
                "private_room_id": private_room_id,
                "invited_user_id": invited_user_id,
            },
            to=room,
        )

    @socketio.on("leave")
    @auth_required
    def on_leave(data):
        user = request.user["name"]
        user_id = request.user["name"]
        
        leave_user(user_id=user_id)
        room = data.get("room")
        leave_room(room)
        emit("active_users", socket_active_users, to=room)
        emit("leave", {"name": user, "user_id": user_id}, to=room)

    @socketio.on("connect")
    @auth_required
    def handle_connect():
        user = request.user["name"]
        user_id = request.user["id"]
        join_user(user_id, user)

    @socketio.on("disconnect")
    @auth_required
    def handle_disconnection():
        leave_user(sid=request.sid)
        for room in rooms(sid=request.sid):
            leave_room(room)

    @socketio.on("set:notification")
    @auth_required
    def set_notification(data):
        """
        This function is used to send notifications to the user.

        Args:
            data (dict): The data sent by the client.

        Returns:
            None

        """
        user_name = request.user["name"]
        user_id_to_notify = data.get("user_id")
        other_data = data.get(
            "additional_data"
        )  # This is for additional data that needs to be sent to the client.
        notification_events = data.get("event_type")
        notification_data = set_notification_data(
            notification_events, user_name, other_data
        )

        for user in socket_active_users:
            if user.get("user_id") == user_id_to_notify:
                sid = user.get("sid")
                emit(
                    "notification",
                    {**notification_data},
                    to=sid,
                )
                break
