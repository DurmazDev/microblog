<template>
  <div
    v-if="!responseData"
    class="flex justify-center mt-4"
  >
    <p v-if="error_message">{{ error_message }}</p>
    <LoadingComponent v-else />
  </div>
  <div
    v-else
    class="max-w-6xl mx-auto mt-4"
  >
    <article
      v-for="(item, index) in responseData"
      :key="index"
      class="p-6 bg-white rounded-lg border border-gray-200 shadow-md"
    >
      <div class="flex justify-between items-center mb-5 text-gray-500">
        <h2 class="mb-2 text-2xl font-bold tracking-tight text-gray-900">
          <a :href="item.url">{{ item.title }}</a>
        </h2>
        <span class="text-sm mb-4"
          >{{
            Math.floor(
              (new Date() - new Date(item.created_at)) / (1000 * 60 * 60 * 24)
            )
          }}
          days ago</span
        >
      </div>
      <p class="mb-5 font-light text-gray-500">{{ item.content }}</p>
      <div class="flex justify-between items-center">
        <a
          :href="item.url"
          class="inline-flex items-center font-medium text-primary-600 hover:underline"
        >
          Read more
          <svg
            class="ml-2 w-4 h-4"
            fill="currentColor"
            viewBox="0 0 20 20"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fill-rule="evenodd"
              d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
              clip-rule="evenodd"
            ></path>
          </svg>
        </a>
      </div>
    </article>
    <div class="mt-4">
      <ul
        v-if="pagination.total_pages > 1"
        class="flex justify-center mt-4 -space-x-px text-sm"
      >
        <li v-if="pagination.prev_page">
          <!-- TODO(ahmet): limit var iken page değiştirilirse limit yok oluyor. -->
          <a
            :href="`?page=${pagination.prev_page}`"
            class="flex items-center justify-center px-3 h-8 ms-0 leading-tight text-gray-500 bg-white border border-e-0 border-gray-300 rounded-s-lg hover:bg-gray-100 hover:text-gray-700"
            >Previous</a
          >
        </li>
        <li
          v-for="(item, index) in pagination.total_pages"
          :key="index"
        >
          <a
            :href="`?page=${item}`"
            class="flex items-center justify-center px-3 h-8 leading-tight text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700"
            >{{ item }}</a
          >
        </li>
        <li v-if="pagination.next_page">
          <a
            :href="`?page=${pagination.next_page}`"
            class="flex items-center justify-center px-3 h-8 leading-tight text-gray-500 bg-white border border-gray-300 rounded-e-lg hover:bg-gray-100 hover:text-gray-700"
            >Next</a
          >
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
  import useFetch from "@/hooks/useFetch.js";
  import LoadingComponent from "./LoadingComponent.vue";

  export default {
    components: { LoadingComponent },

    data() {
      return {
        responseData: null,
        pagination: null,
        error_message: null,
        query_params: [],
      };
    },

    mounted() {
      this.loadData();
    },

    methods: {
      async loadData() {
        let endpoint = "feed";
        const query_params = [];
        const params = new URLSearchParams(
          window.location.search.substring(1)
        );

        if (params.has("page")) {
          query_params.push("page=" + params.get("page"));
        }
        if (params.has("limit")) {
          query_params.push("limit=" + params.get("limit"));
        }

        endpoint += "?" + query_params.join("&");

        try {
          const { data, error } = await useFetch(endpoint);

          if (error.value) {
            this.error_message = error.value;
            return;
          }

          this.responseData = data.value.results;
          this.pagination = data.value.pagination;
        } catch (error) {
          console.error("An error occurred while fetching data:", error.value);
        }
      },
    },
  };
</script>
