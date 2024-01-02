<script setup>
  import { RouterView } from "vue-router";
  import FooterComponent from "./components/FooterComponent.vue";
  import HeaderComponent from "./components/HeaderComponent.vue";
</script>

<template>
  <HeaderComponent />
  <div class="max-w-7xl sm:w-auto mx-auto">
    <RouterView />
  </div>
  <FooterComponent />
</template>
