<template>
  <div class="bg-white border-b border-gray-200 px-4 lg:px-6 py-2.5">
    <div
      class="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl"
    >
      <RouterLink
        class="flex items-center"
        to="/"
      >
        <img
          src="@/assets/icons/Icon.svg"
          class="mr-3 h-6 sm:h-9"
          alt="Logo"
        />
        <span class="self-center text-xl font-semibold whitespace-nowrap">
          MicroBlog
        </span>
      </RouterLink>
      <div
        class="flex items-center lg:order-2"
        v-if="auth"
      >
        <button
          class="text-gray-800 hover:bg-gray-50 focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-4 lg:px-5 py-2 lg:py-2.5 mr-2 focus:outline-none"
          @click="logout"
        >
          Logout
        </button>
        <RouterLink
          to="/profile"
          class="text-gray-800 hover:bg-gray-50 focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-4 lg:px-5 py-2 lg:py-2.5 mr-2 focus:outline-none"
        >
          Profile
        </RouterLink>
        <div>
          <button
            @click="
              this.displayNotificationPopup = !this.displayNotificationPopup
            "
            class="text-gray-800 hover:bg-gray-50 focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm py-2 lg:py-2.5 mr-5 px-2 focus:outline-none"
          >
            <span
              v-if="getUnreadNotificationCount() > 0"
              class="absolute rounded-full bg-red-600 text-white py-0.5 px-2.5 top-1.5 text-[10px]"
            >
              {{ getUnreadNotificationCount() }}
            </span>
            <img
              src="@/assets/icons/notification-bell.svg"
              class="h-6"
              alt="Notification"
            />
          </button>
          <div
            v-if="this.displayNotificationPopup"
            class="absolute w-1/4 border-2 border-gray-200 bg-white shadow-lg rounded-lg p-4 top-14 right-[10%] z-50"
          >
            <div v-if="state.notifications.length != 0">
              <ul>
                <li
                  v-for="(item, index) in state.notifications"
                  :key="index"
                  class="flex items-center cursor-pointer"
                  @click="
                    item.type !== 'private_chat_request' && !item.read
                      ? askJoinPrivateChat(
                          item.notification_id,
                          item.message,
                          item.room_id
                        )
                      : readNotification(item.notification_id)
                  "
                >
                  <span
                    :class="`${item.read ? 'text-gray-500' : 'text-blue-500'} text-3xl`"
                    >&#x2022;</span
                  >
                  <p>{{ item.message }}</p>
                </li>
              </ul>
              <hr class="my-3" />
              <button
                @click="clearNotifications()"
                class="text-center w-full text-blue-600 hover:text-blue-800"
              >
                Clear notifications
              </button>
            </div>
            <span v-else>You do not have any notification.</span>
          </div>
        </div>
        <RouterLink
          to="/create"
          class="text-white bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 font-medium rounded-lg text-sm px-4 lg:px-5 py-2 lg:py-2.5 mr-2 focus:outline-none"
        >
          Create Post
        </RouterLink>
      </div>
      <div
        v-else
        class="flex items-center lg:order-2"
      >
        <RouterLink
          to="/login"
          class="text-gray-800 hover:bg-gray-50 focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-4 lg:px-5 py-2 lg:py-2.5 mr-2 focus:outline-none"
          >Log in
        </RouterLink>
        <RouterLink
          to="/register"
          class="text-white bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 font-medium rounded-lg text-sm px-4 lg:px-5 py-2 lg:py-2.5 mr-2 focus:outline-none"
        >
          Register
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script>
  import { RouterLink } from "vue-router";
  import { state } from "@/services/socket.service";

  export default {
    name: "HeaderComponent",
    components: { RouterLink },
    data() {
      return {
        state: state,
        displayNotificationPopup: false,
        unreadNotificationCount: 0,
      };
    },
    props: {
      auth: {
        type: Boolean,
        required: true,
        default: false,
      },
    },
    methods: {
      logout() {
        this.$store.dispatch("logout");
        this.$router.push({ name: "home" });
      },
      getUnreadNotificationCount() {
        return state.notifications.filter((notification) => !notification.read)
          .length;
      },
      readNotification(notification_id) {
        let notification = state.notifications.find(
          (notification) => notification.notification_id === notification_id
        );
        notification.read = !notification.read;
        localStorage.setItem(
          "notifications",
          JSON.stringify(state.notifications)
        );
      },
      askJoinPrivateChat(notification_id, message, room_id) {
        if (confirm(message)) {
          window.location.href = `/chat#${room_id}`;
          this.readNotification(notification_id);
        }
      },
      clearNotifications() {
        state.notifications = [];
        localStorage.setItem(
          "notifications",
          JSON.stringify(state.notifications)
        );
      },
    },
  };
</script>
