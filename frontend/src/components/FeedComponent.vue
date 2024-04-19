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
    <div
      v-if="this.$store.getters.isAuthenticated"
      class="flex justify-center text-center"
    >
      <div
        :class="`w-1/2 pb-3 border-b-4 ${this.$route.query.q === 'followed' ? 'border-b-blue-500' : ''}`"
      >
        <button
          @click="
            this.$route.query.q = 'followed';
            loadData();
          "
        >
          Followed
        </button>
      </div>
      <div
        :class="`w-1/2 pb-3 border-b-4 ${this.$route.query.q !== 'followed' ? 'border-b-blue-500' : ''}`"
      >
        <button
          @click="
            this.$route.query.q = null;
            loadData();
          "
        >
          Feed
        </button>
      </div>
      <div class="w-1/2 pb-3 border-b-4">
        <RouterLink to="/chat">Live Chat</RouterLink>
      </div>
    </div>
    <ArticleGrid :posts="this.post_list" />
    <PaginationComponents :pagination="this.pagination" />
  </div>
</template>

<script>
  import { RouterLink } from "vue-router";
  import LoadingComponent from "./LoadingComponent.vue";
  import ArticleGrid from "./ArticleComponents/ArticleGrid.vue";
  import { useToast } from "vue-toastify";
  import PaginationComponents from "./PaginationComponents.vue";

  export default {
    components: {
      LoadingComponent,
      ArticleGrid,
      PaginationComponents,
      RouterLink,
    },
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
        this.post_list = [];
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
        if (
          this.$store.getters.isAuthenticated &&
          this.$route.query.q &&
          this.$route.query.q === "followed"
        ) {
          query_params.push("q=followed");
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
        }
      },
    },
  };
</script>
