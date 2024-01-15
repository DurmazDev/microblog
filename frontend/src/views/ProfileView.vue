<template>
  <LoadingComponent v-if="isLoading" />
  <div v-else>
    <p>Your Posts:</p>
    <ArticleGrid
      :posts="posts"
      :allowDelete="true"
      @delete-post="deletePost"
    />
  </div>
</template>

<script>
  import ArticleGrid from "@/components/ArticleComponents/ArticleGrid.vue";
  import LoadingComponent from "@/components/LoadingComponent.vue";
  import { useToast } from "vue-toastify";

  export default {
    name: "ProfileView",
    data() {
      return {
        posts: [],
        isLoading: true,
      };
    },
    methods: {
      deletePost(postID) {
        this.posts = this.posts.filter((post) => post.id !== postID);
      },
      getPosts() {
        this.isLoading = true;
        this.axios
          .get("/post")
          .then((response) => {
            this.posts = response.data;
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
