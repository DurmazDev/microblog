<template>
  <section class="bg-gray-50">
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
          <AlertComponent
            @close="handleCloseAlert"
            :show-alert="alert_data.status"
            :message="alert_data.message.text"
            :type="alert_data.message.type"
          />
          <form class="space-y-4 md:space-y-6">
            <div>
              <label
                for="email"
                class="block mb-2 text-sm font-medium text-gray-900"
                >Your email</label
              >
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
  import useFetch from "@/hooks/useFetch";
  import AlertComponent from "@/components/AlertComponent.vue";

  export default {
    name: "LoginComponent",
    components: { RouterLink, AlertComponent },
    mounted() {
      if (localStorage.getItem("token")) {
        this.$router.push({ name: "home" });
      }
    },
    data() {
      return {
        status: {
          number: null,
          message: null,
        },
        alert_data: {
          status: false,
          message: {
            text: null,
            type: "error",
            required: true,
          },
        },
        error_message: "",
      };
    },
    methods: {
      async login(e) {
        e.preventDefault();
        try {
          if (!this.email || !this.password) {
            this.alert_data.message.text = "Please fill all fields.";
            this.alert_data.message.type = "error";
            this.alert_data.status = true;
            return;
          }
          const { data, error } = await useFetch("auth/login", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              email: this.email,
              password: this.password,
            }),
          });

          if (error.value) {
            this.error_message = error.value;
            this.alert_data.message = error.value;
            this.alert_data.status = true;
            return;
          }
          if (!data) {
            this.error_message = "Something went wrong.";
            this.alert_data.message = "Something went wrong.";
            this.alert_data.status = true;
            return;
          }

          localStorage.setItem("token", data.value.token);
          // store.commit("authenticate", data.value.user);
          this.$router.push({ name: "home" });
        } catch (error) {
          console.log(error);
        }
      },
      handleCloseAlert() {
        this.alert_data.status = false;
      },
    },
  };
</script>
