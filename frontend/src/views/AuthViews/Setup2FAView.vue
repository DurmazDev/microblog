<template>
  <LoadingComponent
    v-if="isLoading"
    class="flex justify-center"
  />
  <section
    v-else
    class="bg-gray-50"
  >
    <div
      class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0"
    >
      <span
        class="flex items-center mb-6 text-2xl font-semibold text-gray-900"
      >
        <img
          class="w-8 h-8 mr-2"
          src="@/assets/icons/Icon.svg"
          alt="logo"
        />
        MicroBlog
      </span>
      <div
        class="w-full bg-white rounded-lg shadow md:mt-0 sm:max-w-md xl:p-0"
      >
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
          <h1
            class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl"
          >
            2FA successfully set, scan QR code & re-login
          </h1>
          <div class="space-y-4 md:space-y-6">
            <div class="flex justify-center">
              <QrcodeVue
                v-if="this.otp_uri"
                :value="this.otp_uri"
                :size="300"
                level="H"
              />
            </div>
            <button
              @click="redirectToReLogin"
              class="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
            >
              Re-Login
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
<script>
  import LoadingComponent from "@/components/LoadingComponent.vue";
  import QrcodeVue from "qrcode.vue";
  import { useToast } from "vue-toastify";

  export default {
    name: "Setup2FAView",
    components: { LoadingComponent, QrcodeVue },
    mounted() {
      this.setup2FA();
    },
    data() {
      return {
        otp_uri: null,
        otp_secret: null,
        isLoading: false,
      };
    },
    methods: {
      redirectToReLogin() {
        this.$store.dispatch("logout").then(() => {
          this.$router.push({ name: "login" });
        });
      },
      setup2FA() {
        this.isLoading = true;
        this.axios
          .get("/auth/setup-2fa")
          .then((response) => {
            this.otp_secret = response.data.secret;
            this.otp_uri = response.data.uri;
            this.isLoading = false;
          })
          .catch((err) => {
            useToast().error(err.response.data.error);
            if (err.response.status === 400) {
              this.$router.push({ name: "profile" });
            }
            return;
          });
      },
    },
  };
</script>
