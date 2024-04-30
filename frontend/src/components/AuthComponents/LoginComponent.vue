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
            Sign in to your account
          </h1>
          <!-- <AlertComponent
            @close="handleCloseAlert"
            :message="this.alert_data.text"
            :type="this.alert_data.type"
            :show-alert="this.alert_data.status"
          /> -->
          <form class="space-y-4 md:space-y-6">
            <div>
              <label
                for="email"
                class="block mb-2 text-sm font-medium text-gray-900"
              >
                Your email
              </label>
              <input
                @change="this.email = $event.target.value"
                type="email"
                name="email"
                id="email"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
                placeholder="name@company.com"
                required=""
              />
            </div>
            <div>
              <label
                for="password"
                class="block mb-2 text-sm font-medium text-gray-900"
                >Password</label
              >
              <input
                @change="this.password = $event.target.value"
                type="password"
                name="password"
                id="password"
                placeholder="••••••••"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
                required=""
              />
            </div>
            <div class="flex items-center justify-between">
              <!--
                TODO(ahmet): Implement forgot password.
                  <a
                  href=""
                  class="text-sm font-medium text-primary-600 hover:underline"
                  >
                  Forgot password?
                </a>
            --></div>
            <button
              @click="login"
              class="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
            >
              Sign in
            </button>
            <p class="text-sm font-light text-gray-500">
              Don’t have an account yet?
              <RouterLink
                to="/register"
                class="font-medium text-primary-600 hover:underline"
              >
                Sign up
              </RouterLink>
            </p>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
  import { RouterLink } from "vue-router";
  import { LOGIN } from "@/stores/auth.module";
  import { useToast } from "vue-toastify";
  import LoadingComponent from "../LoadingComponent.vue";

  export default {
    name: "LoginComponent",
    components: { RouterLink, LoadingComponent },
    mounted() {
      if (this.$store.getters.isAuthenticated) {
        this.$router.push({ name: "home" });
      }
    },
    data() {
      return {
        isLoading: false,
      };
    },
    methods: {
      login(e) {
        this.isLoading = true;
        e.preventDefault();
        try {
          if (!this.email || !this.password) {
            useToast().warning("Please fill all fields.");
            return;
          }
          this.$store
            .dispatch(LOGIN, {
              email: this.email,
              password: this.password,
            })
            .then((response) => {
              if (response.status === 302) {
                this.$router.push({ name: "verify-2fa" });
              } else if (response.status >= 200 && response.status < 300) {
                this.$router.push({ name: "home" });
              }
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
