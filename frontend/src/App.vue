<template>
  <HeaderComponent
    :auth="this.$store.getters.isAuthenticated === true ? true : false"
  />
  <div class="max-w-7xl sm:w-auto mx-auto">
    <RouterView />
  </div>
  <FooterComponent />
</template>

<script>
  import { RouterView } from "vue-router";
  import FooterComponent from "@/components/FooterComponent.vue";
  import HeaderComponent from "@/components/HeaderComponent.vue";
  import { state } from "./services/socket.service";

  export default {
    components: {
      FooterComponent,
      HeaderComponent,
      RouterView,
    },
    mounted() {
      let notifications = localStorage.getItem("notifications");
      if (notifications !== null) {
        state.notifications = JSON.parse(notifications);
      }
    },
  };
</script>
