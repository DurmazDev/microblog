<template>
  <div class="register-view">
    <Register />
  </div>
</template>
<script>
  import Register from "@/components/AuthComponents/RegisterComponent.vue";
  export default {
    name: "RegisterView",
    components: {
      Register,
    },
  };
</script>
