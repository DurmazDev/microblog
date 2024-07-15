<template>
  <ul
    v-if="pagination?.total_pages > 1"
    class="flex justify-center mt-4 -space-x-px text-sm"
  >
    <li v-if="pagination.prev_page">
      <!-- :href="`?page=${pagination.prev_page}`" -->
      <a
        :href="createURLWithPageQueryParam(pagination.prev_page)"
        class="flex items-center justify-center px-3 h-8 ms-0 leading-tight text-gray-500 bg-white border border-e-0 border-gray-300 rounded-s-lg hover:bg-gray-100 hover:text-gray-700"
      >
        Previous
      </a>
    </li>
    <li
      v-for="(item, index) in pagination.total_pages"
      :key="index"
    >
      <a
        :href="createURLWithPageQueryParam(item)"
        class="flex items-center justify-center px-3 h-8 leading-tight text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700"
      >
        {{ item }}
      </a>
    </li>
    <li v-if="pagination.next_page">
      <a
        :href="createURLWithPageQueryParam(pagination.next_page)"
        class="flex items-center justify-center px-3 h-8 leading-tight text-gray-500 bg-white border border-gray-300 rounded-e-lg hover:bg-gray-100 hover:text-gray-700"
      >
        Next
      </a>
    </li>
  </ul>
</template>

<script>
  export default {
    name: "PaginationComponent",
    props: {
      pagination: {
        type: Object,
        required: true,
      },
    },
    methods: {
      createURLWithPageQueryParam(page) {
        const currentQuery = this.$route.query;
        currentQuery.page = page;
        return `?${new URLSearchParams(currentQuery).toString()}`;
      },
    },
  };
</script>
