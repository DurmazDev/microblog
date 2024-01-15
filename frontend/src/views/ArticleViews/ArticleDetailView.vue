<template>
  <div
    v-if="isLoading"
    class="flex justify-center"
  >
    <LoadingComponent />
  </div>
  <ArticleDetails
    v-else
    :article="article"
    @update-comment="updateComment"
    @update-vote="updateVote"
    @delete-comment="deleteComment"
  />
</template>

<script>
  import ArticleDetails from "@/components/ArticleComponents/ArticleDetails.vue";
  import LoadingComponent from "@/components/LoadingComponent.vue";
  import { useToast } from "vue-toastify";

  export default {
    name: "ArticleDetailView",
    components: {
      ArticleDetails,
      LoadingComponent,
    },
    data() {
      return {
        article: {},
        isLoading: true,
      };
    },
    mounted() {
      // Clear articleUrl for safety. (This may cause a bug if the articleUrl contains a special character.)
      this.getArticle(
        this.$route.params.articleUrl.replace(/[^a-zA-Z0-9-]/g, "")
      );
    },
    methods: {
      updateComment(comment) {
        this.article = {
          ...this.article,
          comments: [...this.article.comments, comment],
        };
      },
      deleteComment(comment_id) {
        this.article = {
          ...this.article,
          comments: this.article.comments.filter(
            (comment) => comment.id !== comment_id
          ),
        };
      },
      getArticle(url) {
        this.isLoading = true;
        this.axios
          .get("post/" + url)
          .then((response) => {
            this.article = response.data;
            this.isLoading = false;
          })
          .catch((error) => {
            if (error.response.status === 404)
              this.$router.push({ name: "notfound" });
            useToast().error(error.response.data.error);
            this.isLoading = false;
          });
      },
      updateVote({ voteChange }) {
        this.article = {
          ...this.article,
          vote: this.article.vote + voteChange,
        };
      },
    },
  };
</script>
