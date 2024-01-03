<template>
  <HeaderComponent />
  <div class="max-w-7xl sm:w-auto mx-auto">
    <RouterView />
  </div>
  <FooterComponent />
</template>

<script>
  import { RouterView } from "vue-router";
  import FooterComponent from "@/components/FooterComponent.vue";
  import HeaderComponent from "@/components/HeaderComponent.vue";

  export default {
    components: {
      FooterComponent,
      HeaderComponent,
      RouterView,
    },
  };
</script>
