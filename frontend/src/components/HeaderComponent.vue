<script setup>
  import { RouterLink } from "vue-router";
  defineProps({
    auth: {
      type: Boolean,
      required: true,
      default: false,
    },
  });
</script>

<template>
  <div class="bg-white border-b border-gray-200 px-4 lg:px-6 py-2.5">
    <div
      class="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl"
    >
      <RouterLink
        class="flex items-center"
        to="/"
      >
        <img
          src="./icons/Icon.svg"
          class="mr-3 h-6 sm:h-9"
          alt="Logo"
        />
        <span class="self-center text-xl font-semibold whitespace-nowrap">
          MicroBlog
        </span>
      </RouterLink>
      <div class="flex items-center lg:order-2">
        <RouterLink
          v-if="!auth"
          to="/login"
          class="text-gray-800 hover:bg-gray-50 focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-4 lg:px-5 py-2 lg:py-2.5 mr-2 focus:outline-none"
          >Log in
        </RouterLink>
        <RouterLink
          v-if="!auth"
          to="/register"
          class="text-white bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 font-medium rounded-lg text-sm px-4 lg:px-5 py-2 lg:py-2.5 mr-2 focus:outline-none"
        >
          Register
        </RouterLink>
        <RouterLink
          v-if="auth"
          to="/profile"
          class="text-gray-800 hover:bg-gray-50 focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-4 lg:px-5 py-2 lg:py-2.5 mr-2 focus:outline-none"
        >
          Profile
        </RouterLink>
      </div>
    </div>
  </div>
</template>
