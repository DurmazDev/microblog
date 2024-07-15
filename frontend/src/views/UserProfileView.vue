<template>
  <LoadingComponent v-if="isLoading" />
  <div v-else>
    <div class="flex justify-between">
      <p>{{ user.name }}'s posts:</p>
      <div v-if="this.$store.getters.isAuthenticated">
        <div class="flex">
          <div
            class="flex"
            v-if="user.is_follower"
          >
            <span class="mr-2">{{ user.name }} is your follower</span>
            <button
              @click="removeFollowerEvent"
              class="mx-0.5 text-white font-bold py-2 px-4 rounded inline-flex items-center bg-red-500 hover:bg-red-700"
            >
              Remove
            </button>
          </div>
          <button
            :class="`mx-0.5 text-white font-bold py-2 px-4 rounded inline-flex items-center ${user.is_following ? 'bg-red-500 hover:bg-red-700' : 'bg-green-500 hover:bg-green-700'}`"
            @click="followEvent"
          >
            {{ user.is_following ? "Unfollow" : "Follow" }}
          </button>
        </div>
      </div>
    </div>
    <ArticleGrid :posts="posts" />
  </div>
</template>

<script>
  import ArticleGrid from "@/components/ArticleComponents/ArticleGrid.vue";
  import LoadingComponent from "@/components/LoadingComponent.vue";
  import { useToast } from "vue-toastify";
  import { notificationSender } from "@/services/socket.service";

  export default {
    name: "UserProfileView",
    data() {
      return {
        posts: [],
        user: {},
        isLoading: true,
      };
    },
    methods: {
      removeFollowerEvent() {
        this.axios
          .delete("/user/followers/" + this.$route.params.userID)
          .then(() => {
            this.user.is_follower = false;
            notificationSender(4, this.$route.params.userID);
          })
          .catch((err) => {
            useToast().error(err.response.data.error);
          });
      },
      followEvent() {
        if (this.user.is_following) {
          this.axios
            .delete("/user/" + this.$route.params.userID + "/follow")
            .then(() => {
              this.user.is_following = false;
              notificationSender(1, this.$route.params.userID);
            })
            .catch((err) => {
              useToast().error(err.response.data.error);
            });
          return;
        }
        this.axios
          .post("/user/" + this.$route.params.userID + "/follow")
          .then(() => {
            this.user.is_following = true;
            notificationSender(0, this.$route.params.userID);
          })
          .catch((err) => {
            useToast().error(err.response.data.error);
          });
      },
      getPosts() {
        this.isLoading = true;
        this.axios
          .get("/user/" + this.$route.params.userID + "/post")
          .then((response) => {
            this.posts = response.data.posts;
            this.user = response.data.user;
            this.isLoading = false;
          })
          .catch((err) => {
            if (err.response.status === 404)
              useToast().warning("No posts found.");
            else
              useToast().error("An error occurred. Please try again later.");
            this.isLoading = false;
          });
      },
    },
    mounted() {
      this.getPosts();
    },
    components: { ArticleGrid, LoadingComponent },
  };
</script>
