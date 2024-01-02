<template>
  <div class="max-w-6xl mx-auto">
    <article class="p-6 bg-white rounded-lg border border-gray-200 shadow-md">
      <div class="flex justify-between items-center mb-5 text-gray-500">
        <h2 class="mb-2 text-2xl font-bold tracking-tight text-gray-900">
          <a href="#">Our first project with React</a>
        </h2>
        <span class="text-sm mb-4">14 days ago</span>
      </div>
      <p class="mb-5 font-light text-gray-500">
        Static websites are now used to bootstrap lots of websites and are
        becoming the basis for a variety of tools that even influence both web
        designers and developers influence both web designers and developers.
      </p>
      <div class="flex justify-between items-center">
        <div class="flex items-center space-x-4">
          <img
            class="w-7 h-7 rounded-full"
            src="https://flowbite.s3.amazonaws.com/blocks/marketing-ui/avatars/bonnie-green.png"
            alt="Bonnie Green avatar"
          />
          <span class="font-medium"> Bonnie Green </span>
        </div>
        <a
          href="#"
          class="inline-flex items-center font-medium text-primary-600 hover:underline"
        >
          Read more
          <svg
            class="ml-2 w-4 h-4"
            fill="currentColor"
            viewBox="0 0 20 20"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fill-rule="evenodd"
              d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
              clip-rule="evenodd"
            ></path>
          </svg>
        </a>
      </div>
    </article>
  </div>
  <p>{{ responseData }}</p>
</template>

<script>
  export default {
    data() {
      return {
        responseData: null,
      };
    },
    mounted() {
      this.fetchData();
    },
    methods: {
      async fetchData() {
        try {
          const response = await fetch("http://127.0.0.1:8000/feed"); // API endpoint'inizi buraya ekleyin
          const data = await response.json();

          // API yanıtını responseData verisine atayın
          this.responseData = data;
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      },
    },
  };
</script>
