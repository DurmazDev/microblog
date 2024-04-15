<template>
  <div class="flex mt-4">
    <div class="w-5/6">
      <div class="flex justify-between mr-2">
        <p>
          Connection status:
          {{ this.state.connected ? "Established" : "Not established" }}
        </p>
        <span
          v-if="this.private_room_uri === null"
          class="text-white bg-blue-700 hover:bg-blue-800 font-medium rounded-lg text-sm px-4 py-0.5"
          @click="private_handler()"
          >Create Private Room</span
        >
      </div>
      <div
        id="messages"
        class="border rounded mr-2 h-80 flex flex-col-reverse overflow-scroll"
      >
        <div>
          <div
            v-for="(item, index) in messages()"
            v-bind:key="index"
          >
            <div
              :class="`flex flex-col-reverse ${item.user_id === this.$store.getters.currentUser.id ? 'items-end' : 'items-start'} gap-2.5 my-1 ml-1`"
            >
              <div
                :class="`flex flex-col max-w-[540px] break-words leading-1.5 p-4 ${item.user_id === this.$store.getters.currentUser.id ? 'border-indigo-200 bg-indigo-100' : 'border-gray-200 bg-gray-100'} rounded-s-xl rounded-se-xl`"
              >
                <div class="flex items-center space-x-2 rtl:space-x-reverse">
                  <span
                    :id="`${item.user_id}`"
                    class="text-sm font-semibold text-gray-900"
                    >{{ item.name }}</span
                  >
                  <span class="text-sm font-normal text-gray-500">{{
                    new Date(item.date).toLocaleTimeString()
                  }}</span>
                </div>
                <p class="text-sm font-normal py-2.5 text-gray-900">
                  {{ item.message }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="w-1/6">
      <p>Active users in whole chat (click for invite to private chat):</p>
      <div class="border rounded overflow-scroll">
        <div class="max-h-80 min-h-72">
          <ul>
            <li
              v-for="(item, index) in this.state.users"
              v-bind:key="index"
              @click="invite_private_chat(item.user_id)"
            >
              {{ item.name }}
              {{
                item.id === this.$store.getters.currentUser.id ? "(You)" : null
              }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
  <div>
    <form
      class="flex mt-2"
      @submit="(e) => message(e)"
    >
      <input
        type="text"
        id="send"
        ref="send"
        class="block w-full mr-2 p-2 ps-5 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50"
        placeholder="Send"
        required
      />
      <button
        type="submit"
        class="text-white bg-blue-700 hover:bg-blue-800 font-medium rounded-lg text-sm px-4 py-2"
      >
        Send
      </button>
    </form>
    <div class="w-full flex justify-center">
      <div
        v-if="
          this.private_room_uri !== null && this.private_room_hash !== null
        "
        class="flex justify-center mt-2 w-full md:w-1/2 mr-2 p-2 ps-5 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50"
      >
        <div>
          <span>Share this URL with your friend:</span>
          <a
            :href="this.private_room_uri"
            class="text-blue-700 hover:text-blue-800 mr-4 ml-2"
          >
            {{ this.private_room_uri }}
          </a>
          <button
            class="text-white bg-blue-700 hover:bg-blue-800 font-medium rounded-lg text-sm px-4 py-2"
            @click="this.copyToClipboard(this.private_room_uri)"
          >
            Copy Link
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import { io } from "socket.io-client";
  import config from "@/config";
  import { getToken } from "@/services/jwt.service";
  import { useToast } from "vue-toastify";

  export default {
    name: "ChatView",
    created() {
      window.addEventListener("beforeunload", this.leaving);
    },
    data() {
      return {
        room: "public-room",
        state: {
          connected: false,
          messages: [],
          users: [],
        },
        private_room_uri: null,
        private_room_hash: null,
        socket: io(config.apiUrl),
      };
    },
    computed: {
      connected() {
        return this.state.connected;
      },
    },
    mounted() {
      this.socket.on("connect", () => {
        this.state.connected = true;
      });

      this.socket.on("disconnect", () => {
        this.state.connected = false;
      });

      this.socket.on("message", (data) => {
        this.state.messages.push({
          user_id: data.user_id,
          name: data.name,
          message: data.message,
          date: new Date().getTime(),
        });
      });

      this.socket.on("active_users", (data) => {
        this.state.users = data;
      });

      this.socket.on("private_chat_request", (data) => {
        if (data.invited_user_id !== this.$store.getters.currentUser.id)
          return;
        if (
          confirm(`${data.name} invited you to a private chat. Do you accept?`)
        ) {
          this.leaving();
          this.state.messages = [];
          this.room = data.private_room_id;
          window.location.hash = data.private_room_id;
          this.join();
          useToast().info("Successfully connected.");
        }
      });

      if (window.location.hash && !this.state.connected) {
        this.private_handler(window.location.hash);
      } else {
        this.join();
      }
    },
    methods: {
      private_handler(hash) {
        if (hash === undefined) {
          let room_hash = [...Array(7)]
            .map(() => Math.floor(Math.random() * 16).toString(16))
            .join("");
          this.private_room_hash = room_hash;
          this.private_room_uri =
            window.location.origin + "/chat#" + room_hash;
          window.location.hash = room_hash;

          this.leaving();
          this.state.messages = [];
          this.room = room_hash;
          this.join();
          return room_hash;
        }
        this.leaving();
        this.state.messages = [];
        this.room = hash.substring(1);
        this.join();
      },
      invite_private_chat(id) {
        if (this.room !== "public-room") {
          useToast().error("You are already in private chat room.");
          return;
        }
        if (id == this.$store.getters.currentUser.id) {
          useToast().error("You cannot invite yourself to chat.");
          return;
        }
        let tempRoom = this.room;
        let newRoomHash = this.private_handler();
        this.socket.emit("private_chat_request", {
          token: getToken(),
          room: tempRoom,
          private_room_id: newRoomHash,
          invited_user_id: id,
        });
        useToast().info("Request sent.");
      },
      leaving() {
        this.socket.emit("leave", {
          token: getToken(),
          room: this.room,
        });
      },
      messages() {
        return this.state.messages;
      },
      join() {
        this.socket.emit("join", {
          token: getToken(),
          room: this.room,
        });
      },
      message(e) {
        e.preventDefault();
        this.socket.emit("message", {
          token: getToken(),
          room: this.room,
          message: this.$refs.send.value.trim(),
        });
        this.$refs.send.value = "";
      },
      copyToClipboard(text) {
        navigator.clipboard.writeText(text);
      },
    },
  };
</script>
