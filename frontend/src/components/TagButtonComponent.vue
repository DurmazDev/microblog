<template>
  <div v-if="tag">
    <div v-if="this.$route.name === 'home'">
      <a
        :href="`/?tag=${tag}`"
        class="mx-0.5 bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center"
      >
        {{ tag }}
      </a>
    </div>
    <div v-else>
      <RouterLink
        :to="`/?tag=${tag}`"
        class="mx-0.5 bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center"
      >
        {{ tag }}
      </RouterLink>
    </div>
  </div>
</template>

<script>
  export default {
    mounted() {
      console.log(this.$route);
    },
    props: {
      tag: {
        type: String,
        default: null,
        required: true,
      },
    },
  };
</script>
