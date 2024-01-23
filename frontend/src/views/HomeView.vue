<template>
  <div class="home-view">
    <FeedComponent />
  </div>
</template>

<script>
  import FeedComponent from "@/components/FeedComponent.vue";

  export default {
    name: "HomeView",
    components: {
      FeedComponent,
    },
  };
</script>
