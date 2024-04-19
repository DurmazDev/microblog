<template>
  <div
    v-if="showAlert"
    :class="`flex justify-between p-4 mb-4 text-sm border rounded-lg text-${selectedColor}-800 border-${selectedColor}-300 bg-${selectedColor}-50`"
    role="alert"
  >
    <div class="flex">
      <img
        src="@/assets/icons/right-arrow.svg"
        class="flex-shrink-0 inline w-4 h-4 me-3"
        alt="Notification"
      />
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
      type: {
        type: String,
        default: "error", // Allowed: success, error, warning, info
        required: true,
      },
      showAlert: {
        type: Boolean,
        required: true,
      },
      message: {
        type: String,
        required: true,
      },
    },
    data() {
      return {
        selectedColor: "blue",
      };
    },
    mounted() {
      this.setColor();
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
        this.selectedColor = color;
      },
    },
  };
</script>
