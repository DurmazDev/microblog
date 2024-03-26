<template>
  <div v-if="this.followings.length > 0 && this.followers.length > 0">
    <div class="flex">
      <p class="w-1/2 text-2xl">Followers</p>
      <p class="w-1/2 text-2xl">Followings</p>
    </div>
    <div class="flex">
      <div class="border-2 rounded w-1/2 grid grid-cols-4">
        <RouterLink
          v-for="(item, key) in this.followers"
          v-bind:key="key"
          :to="`/profile/${item.id}`"
          class="text-center"
        >
          <span class="text-xs">{{ item.name }}</span>
        </RouterLink>
      </div>
      <div class="border-2 rounded w-1/2 grid grid-cols-4">
        <RouterLink
          v-for="(item, key) in this.followings"
          v-bind:key="key"
          :to="`/profile/${item.id}`"
          class="text-center"
        >
          <span class="text-xs">{{ item.name }}</span>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script>
  import { RouterLink } from "vue-router";

  export default {
    props: {
      followers: {
        type: Array,
        required: true,
      },
      followings: {
        type: Array,
        required: true,
      },
    },
    components: {
      RouterLink,
    },
  };
</script>
