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
            Enter your 2FA code from Authenticator App
          </h1>
          <form class="space-y-4 md:space-y-6">
            <div>
              <label
                for="verificationCode"
                class="block mb-2 text-sm font-medium text-gray-900"
              >
                6-Digit 2FA Code
              </label>
              <input
                @change="this.verificationCode = $event.target.value"
                type="number"
                name="verificationCode"
                id="verificationCode"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
                placeholder="••••••"
                required=""
              />
            </div>
            <button
              @click="verify2FA"
              class="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
            >
              Sign in
            </button>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>
<script>
  import LoadingComponent from "@/components/LoadingComponent.vue";
  import { VERIFY_2FA } from "@/stores/auth.module";
  import { getToken } from "@/services/jwt.service";
  import { useToast } from "vue-toastify";

  export default {
    name: "Verify2FAView",
    components: { LoadingComponent },
    mounted() {
      if (this.$store.getters.isAuthenticated) {
        this.$router.push({ name: "home" });
      }
      if (getToken() === null) {
        this.$router.push({ name: "login" });
      }
    },
    data() {
      return {
        verificationCode: 0,
        isLoading: false,
      };
    },
    methods: {
      verify2FA(e) {
        e.preventDefault();
        this.isLoading = true;
        if (this.verificationCode.toString().length !== 6) {
          this.isLoading = false;
          useToast().error("Please enter a valid 6-digit code.");
          return;
        }
        try {
          this.$store
            .dispatch(VERIFY_2FA, this.verificationCode)
            .then(() => {
              this.$router.push({ name: "home" });
            })
            .catch(() => {
              useToast().error(this.$store.getters.errorMessages);
              return;
            });
        } catch (error) {
          useToast().error("An error occurred. Please try again later.");
        }
        this.isLoading = false;
      },
    },
  };
</script>
