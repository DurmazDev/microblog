from app.utils import decode_token
from flask_socketio import emit, rooms, join_room, leave_room


def handle_socketio_requests(socketio, app):
    socket_active_users = []

    @socketio.on("active_users")
    def get_active_users(data):
        token = data.get("token")
        if token == None:
            return
        try:
            decode_token(token)
        except Exception as e:
            app.logger.error(e)
            return
        emit("active_users", {"users": socket_active_users})

    @socketio.on("message")
    def handle_message(data):
        token = data.get("token")
        if token == None:
            return
        try:
            user_data = decode_token(token)
        except Exception as e:
            app.logger.error(e)
            return

        user = user_data.get("name")
        user_id = user_data.get("id")
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
    def on_join(data):
        token = data.get("token")
        if token == None:
            return
        try:
            user_data = decode_token(token)
        except Exception as e:
            app.logger.error(e)
            return

        user = user_data.get("name")
        user_id = user_data.get("id")
        if {"name": user, "user_id": user_id} not in socket_active_users:
            socket_active_users.append({"name": user, "user_id": user_id})
        room = data.get("room")

        join_room(room)
        emit("active_users", socket_active_users, to=room)
        emit("join", {"name": user, "user_id": user_id}, to=room)

    @socketio.on("private_chat_request")
    def on_private_chat_request(data):
        token = data.get("token")
        if token == None:
            return
        try:
            user_data = decode_token(token)
        except Exception as e:
            app.logger.error(e)
            return

        user = user_data.get("name")
        user_id = user_data.get("id")
        private_room_id = data.get("private_room_id")
        invited_user_id = data.get("invited_user_id")
        room = data.get("room")
        if room == None:
            return
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
    def on_leave(data):
        token = data.get("token")
        if token == None:
            return
        try:
            user_data = decode_token(token)
        except Exception as e:
            app.logger.error(e)
            return

        user = user_data.get("name")
        user_id = user_data.get("id")
        if {"name": user, "user_id": user_id} in socket_active_users:
            socket_active_users.remove({"name": user, "user_id": user_id})
        room = data.get("room")

        leave_room(room)
        emit("active_users", socket_active_users, to=room)
        emit("leave", {"name": user, "user_id": user_id}, to=room)
