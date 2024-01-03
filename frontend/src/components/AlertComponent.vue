<template>
  <div
    v-if="showAlert"
    :class="`flex justify-between p-4 mb-4 text-sm border rounded-lg text-${setColor()}-800 border-${setColor()}-300 bg-${setColor()}-50`"
    role="alert"
  >
    <div class="flex">
      <svg
        class="flex-shrink-0 inline w-4 h-4 me-3"
        aria-hidden="true"
        xmlns="http://www.w3.org/2000/svg"
        fill="currentColor"
        viewBox="0 0 20 20"
      >
        <path
          d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"
        />
      </svg>
      <div>
        <span class="font-medium">{{ message }}</span>
      </div>
    </div>
    <div>
      <button
        class="close-btn"
        @click="closeAlert"
      >
        X
      </button>
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      showAlert: {
        type: Boolean,
        required: true,
      },
      type: {
        type: String,
        default: "info", // Allowed: success, error, warning, info
        required: true,
      },
      message: {
        type: String,
        default: "Something went wrong!",
        required: true,
      },
    },
    data() {
      return {
        color: this.type,
      };
    },
    methods: {
      closeAlert() {
        this.$emit("close");
      },
      setColor() {
        let color = "";
        if (this.type === "error") {
          color = "red";
        } else if (this.type === "warning") {
          color = "yellow";
        } else if (this.type === "success") {
          color = "green";
        } else {
          color = "blue";
        }
        return color;
      },
    },
  };
</script>
