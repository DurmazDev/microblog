import { io } from "socket.io-client";
import { reactive } from "vue";
import { useToast } from "vue-toastify";
import store from "@/stores";
import config from "@/config";
import { getToken } from "./jwt.service";

export const state = reactive({
  connected: false,
  endpoints_implemented: false,
  room: "public-room",
  messages: [],
  notifications: [],
  users: [],
});

let socket = io(config.apiUrl, {
  extraHeaders: { Authorization: getToken() },
});

socket.on("connect", () => {
  state.connected = socket.connected;
});

socket.on("disconnect", () => {
  state.connected = false;
});

socket.on("notification", (data) => {
  data.time = new Date().getTime();
  if (data.message.endsWith("has sent you a private chat request.")) {
    data.type = "private_chat_request";
  }
  state.notifications.push(data);
  state.notifications.sort((a, b) => b.time - a.time);
  // Save last 25 notifications to local storage
  localStorage.setItem(
    "notifications",
    JSON.stringify(state.notifications.slice(-25))
  );
});

socket.on("message", (data) => {
  state.messages.push({
    user_id: data.user_id,
    name: data.name,
    message: data.message,
    date: new Date().getTime(),
  });
});

socket.on("active_users", (data) => {
  state.users = data;
});

socket.on("private_chat_request", (data) => {
  if (data.invited_user_id !== store.getters.currentUser.id) return;
  if (confirm(`${data.name} invited you to a private chat. Do you accept?`)) {
    leaving();
    state.messages = [];
    state.room = data.private_room_id;
    window.location.hash = data.private_room_id;
    join();
    useToast().info("Successfully connected.");
  }
});

function join() {
  socket.emit("join", {
    room: state.room,
  });
}

function leaving() {
  socket.emit("leave", {
    room: state.room,
  });
  state.room = "public-room";
  state.messages = [];
}
function notificationSender(eventType, userID, additionalData = null) {
  /**
   * Send a notification to the server.
   *
   * @param {number} eventType - The type of the event. This should be a constant defined in the server.
   * @param {string} userID - The user id of the user to notify.
   * @param {object|null} [additionalData=null] - Any additional data that should be sent with the notification.
   *
   * @typedef {object} AdditionalData
   * @property {string} user_id - The user id of the user to notify.
   * @property {string} [post_id] - The additional_data object includes post_id.
   * @property {string} [room_id] - The additional_data object includes room_id.
   *
   *  0: Follow
   *  Args:
   *      user_id: The user id of the user to notify.
   *  1: Unfollow
   *  Args:
   *      user_id: The user id of the user to notify.
   *  2: Private Chat Request
   *  Args:
   *      user_id: The user id of the user to notify.
   *      additional_data: The additional_data object includes room_id.
   *  3: Voted Your Post
   *  Args:
   *      user_id: The user id of the user to notify.
   *  4: Removed you from their followers list
   *  Args:
   *      user_id: The user id of the user to notify.
   *  5: Commented on your post
   *  Args:
   *      user_id: The user id of the user to notify.
   *      post_id: The additional_data object includes post_id.
   * @example
   * // Follow event
   * notificationSender(0, "ObjectId()");
   *
   * // Private Chat Request event
   * notificationSender(2, "ObjectId()", { user_id: "ObjectId()", {room_id: "room123"} });
   */
  let data = {
    event_type: eventType,
    user_id: userID,
  };
  if (additionalData !== null && typeof additionalData === "object") {
    data.additional_data = additionalData;
  }
  socket.emit("set:notification", data);
}

export { socket, notificationSender, join, leaving };
