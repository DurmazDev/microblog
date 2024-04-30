<template>
  <div class="mt-2">
    <p class="text-2xl">Settings</p>
    <div class="border-2 rounded w-full grid grid-cols-4">
      <form>
        <div class="flex">
          <span class="mr-2">2FA: </span>
          <input
            name="radio-2fa"
            id="2fa_disabled"
            type="radio"
            @change="handle2FA"
            :disabled="!this.$store.getters.is2FAEnabled"
          />
          <label
            for="2fa_disabled"
            class="ml-1"
            >Disabled</label
          >
          <input
            name="radio-2fa"
            class="ml-4"
            id="2fa_enabled"
            type="radio"
            @change="handle2FA"
            :disabled="this.$store.getters.is2FAEnabled"
          />
          <label
            for="2fa_enabled"
            class="ml-1"
            >Enabled</label
          >
        </div>
      </form>
    </div>
  </div>
</template>
<script>
  import { useToast } from "vue-toastify";
  import { SET_2FA_STATUS } from "@/stores/auth.module";

  export default {
    name: "SettingsComponent",
    mounted() {
      if (this.$store.getters.is2FAEnabled) {
        document.getElementById("2fa_enabled").checked = true;
      } else {
        document.getElementById("2fa_disabled").checked = true;
      }
    },
    methods: {
      handle2FA(e) {
        e.preventDefault();
        if (e.target.id === "2fa_disabled" && e.target.checked) {
          this.axios({
            method: "delete",
            url: "/auth/setup-2fa",
          })
            .then((response) => {
              if (response.status === 200) {
                this.$store.dispatch(SET_2FA_STATUS, false);
                useToast().warning("2FA has been disabled.");
                return;
              }
            })
            .catch(() => {
              useToast().error("An error occurred. Please try again later.");
              return;
            });
          return;
        }
        if (!this.$store.getters.is2FAEnabled) {
          this.$router.push("/setup-2fa");
          return;
        }
      },
    },
  };
</script>
