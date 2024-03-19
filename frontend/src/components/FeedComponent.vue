<template>
  <div
    v-if="isLoading"
    class="flex justify-center mt-4"
  >
    <p v-if="error_message">{{ error_message }}</p>
    <LoadingComponent v-else />
  </div>
  <div
    v-else
    class="max-w-6xl mx-auto mt-4"
  >
    <ArticleGrid :posts="this.post_list" />
    <PaginationComponents :pagination="this.pagination" />
  </div>
</template>

<script>
  import LoadingComponent from "./LoadingComponent.vue";
  import ArticleGrid from "./ArticleComponents/ArticleGrid.vue";
  import { useToast } from "vue-toastify";
  import PaginationComponents from "./PaginationComponents.vue";

  export default {
    components: { LoadingComponent, ArticleGrid, PaginationComponents },
    data() {
      return {
        post_list: [],
        pagination: null,
        error_message: null,
        query_params: [],
        isLoading: true,
      };
    },
    mounted() {
      this.loadData();
    },
    methods: {
      loadData() {
        this.isLoading = true;
        let endpoint = "feed";
        const query_params = [];

        if (this.$route.query.page) {
          query_params.push("page=" + this.$route.query.page);
        }
        if (this.$route.query.limit) {
          query_params.push("limit=" + this.$route.query.limit);
        }
        if (this.$route.query.tag) {
          query_params.push("tag=" + this.$route.query.tag);
        }

        endpoint += "?" + query_params.join("&");

        try {
          this.axios
            .get(endpoint)
            .then((response) => {
              this.post_list = response.data.results;
              this.pagination = response.data.pagination;
              this.isLoading = false;
            })
            .catch((error) => {
              if (error.response.status === 404) {
                useToast().info(error.response.data.error);
              } else {
                useToast().error(error.response.data.error);
              }
              this.isLoading = false;
            });
        } catch (error) {
          this.isLoading = false;
          useToast().error(
            "An error occurred while fetching data:",
            error.value
          );
          // console.error("An error occurred while fetching data:", error.value);
        }
      },
    },
  };
</script>
