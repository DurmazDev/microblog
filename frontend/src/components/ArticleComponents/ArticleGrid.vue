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
        <RouterLink :to="'/' + item.url.replace(config.frontendUrl, '')">{{
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
      <div>
        <RouterLink
          :to="item.url.replace(config.frontendUrl, '')"
          class="mb-1 inline-flex items-center font-medium text-primary-600 hover:underline"
        >
          Read more
          <img
            src="@/assets/icons/right-arrow.svg"
            class="ml-2 w-4 h-4"
            alt="Notification"
          />
        </RouterLink>
        <br />
        <div v-if="item.author">
          <RouterLink
            class="text-gray-500 hover:underline"
            :to="`/profile/${item.author.id}`"
          >
            Author: {{ item.author.name }}
          </RouterLink>
        </div>
      </div>
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
          <img
            height="20px"
            width="20px"
            src="@/assets/icons/trash.svg"
            alt="trash"
          />
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
