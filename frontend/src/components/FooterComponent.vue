<script setup>
  import { RouterLink } from "vue-router";
</script>
<template>
  <div class="bg-white rounded-lg shadow m-4">
    <div class="w-full max-w-screen-xl mx-auto p-4 md:py-8">
      <div class="sm:flex sm:items-center sm:justify-between">
        <RouterLink
          to="/"
          class="flex items-center mb-4 sm:mb-0 space-x-3 rtl:space-x-reverse"
        >
          <img
            src="./icons/Icon.svg"
            class="h-8"
            alt="Logo"
          />
          <span class="self-center text-2xl font-semibold whitespace-nowrap">
            MicroBlog
          </span>
        </RouterLink>
        <ul
          class="flex flex-wrap items-center mb-6 text-sm font-medium text-gray-500 sm:mb-0"
        >
          <li>
            <RouterLink
              to="/about"
              class="hover:underline me-4 md:me-6"
            >
              About
            </RouterLink>
          </li>
          <li>
            <RouterLink
              to="/privacy-policy"
              class="hover:underline me-4 md:me-6"
            >
              Privacy Policy
            </RouterLink>
          </li>
        </ul>
      </div>
      <hr class="my-6 border-gray-200 sm:mx-auto lg:my-8" />
      <span class="block text-sm text-gray-500 sm:text-center"
        >© 2023
        <RouterLink
          to="/"
          class="hover:underline"
        >
          MicroBlog™.
        </RouterLink>
        All Rights Reserved (are they?)</span
      >
    </div>
  </div>
</template>
