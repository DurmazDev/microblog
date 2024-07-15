<template>
  <div class="login-view">
    <Login />
  </div>
</template>
<script>
  import Login from "@/components/AuthComponents/LoginComponent.vue";
  export default {
    name: "LoginView",
    components: {
      Login,
    },
  };
</script>
