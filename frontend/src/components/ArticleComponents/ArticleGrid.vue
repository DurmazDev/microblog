<template>
  <div v-if="posts.length < 1">No posts found.</div>
  <article
    v-else
    v-for="(item, index) in posts"
    :key="index"
    class="p-6 bg-white rounded-lg border border-gray-200 shadow-md"
  >
    <div class="flex justify-between items-center mb-5 text-gray-500">
      <h2 class="mb-2 text-2xl font-bold tracking-tight text-gray-900">
        <RouterLink :to="item.url.replace(config.frontendUrl, '')">{{
          item.title
        }}</RouterLink>
      </h2>
      <span class="text-sm mb-4">
        {{ formatDate(item.created_at) }}
      </span>
    </div>
    <p
      v-if="item.content"
      class="mb-5 font-light text-gray-500"
    >
      {{ item.content?.replace(/(<([^>]+)>)/gi, "") }}
    </p>
    <div class="flex justify-between items-center">
      <RouterLink
        :to="item.url.replace(config.frontendUrl, '')"
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
      </RouterLink>
      <div class="flex">
        <TagButton
          :v-if="item.tags"
          v-for="(tag, index) in item.tags"
          :key="index"
          :tag="tag.name"
        />
        <button
          v-if="allowDelete"
          @click="deletePost(item.id)"
          class="flex"
        >
          <svg
            fill="#000000"
            height="20px"
            width="20px"
            version="1.1"
            id="Layer_1"
            viewBox="0 0 354.319 354.319"
            xml:space="preserve"
          >
            <path
              id="XMLID_2_"
              d="M293.765,125.461l-41.574-17.221l17.221-41.574c3.17-7.654-0.464-16.428-8.118-19.599L150.428,1.146
        C142.775-2.024,134,1.61,130.83,9.264l-17.221,41.574L72.035,33.617c-7.654-3.17-16.428,0.464-19.599,8.118
        c-3.17,7.654,0.464,16.428,8.118,19.599l55.433,22.961l96.628,40.024H87.16c-8.284,0-15,6.716-15,15v200c0,8.284,6.716,15,15,15h180
        c8.284,0,15-6.716,15-15V153.126l0.125,0.052c1.877,0.777,3.821,1.146,5.734,1.146c5.886,0,11.472-3.487,13.864-9.264
        C305.053,137.406,301.419,128.631,293.765,125.461z M141.326,62.318l11.48-27.716l83.148,34.441l-11.48,27.716L182.9,79.539
        L141.326,62.318z"
            />
          </svg>
          Delete Post
        </button>
      </div>
    </div>
  </article>
</template>

<script>
  import { RouterLink } from "vue-router";
  import config from "@/config";
  import { useToast } from "vue-toastify";
  import TagButton from "../TagButtonComponent.vue";

  export default {
    name: "ArticleGrid",
    data() {
      return {
        config,
      };
    },
    props: {
      posts: {
        type: Array,
        required: true,
      },
      allowDelete: {
        type: Boolean,
        required: false,
      },
    },
    methods: {
      deletePost(id) {
        this.axios({
          method: "delete",
          url: "post/" + id,
        })
          .then((response) => {
            if (response.status === 204) {
              this.$emit("delete-post", id);
              useToast().info("Post deleted successfully.");
              // this.$router.go(this.$router.currentRoute);
            }
          })
          .catch(() => {
            useToast().error("An error occurred. Please try again later.");
          });
      },
      formatDate(date) {
        date = Math.floor(
          (new Date() - new Date(date)) / (1000 * 60 * 60 * 24)
        );
        if (date === 0) {
          return "Today";
        } else if (date === 1) {
          return "Yesterday";
        } else {
          return date + " days ago";
        }
      },
    },
    components: { RouterLink, TagButton },
  };
</script>
