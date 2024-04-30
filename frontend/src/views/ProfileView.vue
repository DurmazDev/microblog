<template>
  <LoadingComponent v-if="isLoading !== 3" />
  <div v-else>
    <p>Your Posts:</p>
    <ArticleGrid
      :posts="posts"
      :allowDelete="true"
      @delete-post="deletePost"
    />
    <FollowerViewerComponent
      :followers="followers"
      :followings="followings"
    />
    <SettingsComponent />
  </div>
</template>

<script>
  import ArticleGrid from "@/components/ArticleComponents/ArticleGrid.vue";
  import FollowerViewerComponent from "@/components/FollowerViewerComponent.vue";
  import LoadingComponent from "@/components/LoadingComponent.vue";
  import SettingsComponent from "@/components/SettingsComponent.vue";
  import { useToast } from "vue-toastify";

  export default {
    name: "ProfileView",
    data() {
      return {
        posts: [],
        isLoading: 0,
        followers: [],
        followings: [],
      };
    },
    methods: {
      getFollowers() {
        this.axios
          .get("/user/followers")
          .then((response) => {
            this.followers = response.data;
            this.isLoading += 1;
          })
          .catch((err) => {
            if (err.response.status === 404) {
              this.isLoading += 1;
              return;
            }
            useToast().error("An error occurred. Please try again later.");
            this.isLoading += 1;
          });
      },
      getFollowings() {
        this.axios
          .get("/user/followings")
          .then((response) => {
            this.followings = response.data;
            this.isLoading += 1;
          })
          .catch((err) => {
            if (err.response.status === 404) {
              this.isLoading += 1;
              return;
            }
            useToast().error("An error occurred. Please try again later.");
            this.isLoading += 1;
          });
      },
      deletePost(postID) {
        this.posts = this.posts.filter((post) => post.id !== postID);
      },
      getPosts() {
        this.axios
          .get("/post")
          .then((response) => {
            this.posts = response.data;
            this.isLoading += 1;
          })
          .catch((err) => {
            if (err.response.status === 404)
              useToast().warning("No posts found.");
            else
              useToast().error("An error occurred. Please try again later.");
            this.isLoading += 1;
          });
      },
    },
    mounted() {
      this.getPosts();
      this.getFollowers();
      this.getFollowings();
    },
    components: {
      ArticleGrid,
      LoadingComponent,
      FollowerViewerComponent,
      SettingsComponent,
    },
  };
</script>
