<template>
  <section class="bg-gray-50">
    <div
      class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0"
    >
      <a
        href="#"
        class="flex items-center mb-6 text-2xl font-semibold text-gray-900"
      >
        <img
          class="w-8 h-8 mr-2"
          src="@/assets/icons/Icon.svg"
          alt="logo"
        />
        MicroBlog
      </a>
      <div
        class="w-full bg-white rounded-lg shadow md:mt-0 sm:max-w-md xl:p-0"
      >
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
          <h1
            class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl"
          >
            Create and account
          </h1>
          <AlertComponent
            @close="handleCloseAlert"
            :show-alert="alert_data.status"
            :message="alert_data.message"
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
                for="name"
                class="block mb-2 text-sm font-medium text-gray-900"
                >Your name</label
              >
              <input
                @change="this.name = $event.target.value"
                type="name"
                name="name"
                id="name"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
                placeholder="John Doe"
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
            <div>
              <label
                for="confirm-password"
                class="block mb-2 text-sm font-medium text-gray-900"
                >Confirm password</label
              >
              <input
                @change="this.confirmPassword = $event.target.value"
                type="password"
                name="confirm-password"
                id="confirm-password"
                placeholder="••••••••"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
                required=""
              />
            </div>
            <div class="flex items-start">
              <div class="flex items-center h-5">
                <input
                  @change="this.terms = $event.target.checked"
                  id="terms"
                  aria-describedby="terms"
                  type="checkbox"
                  class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-primary-300"
                  required=""
                />
              </div>
              <div class="ml-3 text-sm">
                <label
                  for="terms"
                  class="font-light text-gray-500"
                >
                  I accept the
                  <span class="font-medium text-primary-600 hover:underline">
                    Terms and Conditions
                  </span>
                </label>
              </div>
            </div>
            <button
              @click="register"
              class="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
            >
              Create an account
            </button>
            <p class="text-sm font-light text-gray-500">
              Already have an account?
              <RouterLink
                to="/login"
                class="font-medium text-primary-600 hover:underline"
              >
                Login here
              </RouterLink>
            </p>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>
<script>
  import AlertComponent from "@/components/AlertComponent.vue";
  import { RouterLink } from "vue-router";
  import useFetch from "@/hooks/useFetch";

  export default {
    name: "RegisterView",
    components: {
      RouterLink,
      AlertComponent,
    },
    mounted() {
      if (localStorage.getItem("token")) {
        this.$router.push({ name: "home" });
      }
    },
    data() {
      return {
        email: null,
        name: null,
        password: null,
        confirmPassword: null,
        terms: false,
        alert_data: {
          status: false,
          message: null,
        },
        error_message: null,
      };
    },
    methods: {
      async register(e) {
        e.preventDefault();
        try {
          this.alert_data.status = false;
          if (!this.terms) {
            this.alert_data.message =
              "You must accept the terms and conditions.";
            this.alert_data.status = true;
            return;
          }
          if (this.password !== this.confirmPassword) {
            this.alert_data.message = "Passwords do not match.";
            this.alert_data.status = true;
            return;
          }
          const { data, error } = await useFetch("auth/register", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              name: this.name,
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
            this.alert_data.message = "Something went wrong.";
            this.alert_data.status = true;
            return;
          }

          localStorage.setItem("token", data.value.token);
          this.$router.push({ name: "home" });
        } catch (err) {
          console.log(err);
        }
      },
      handleCloseAlert() {
        this.alert_data.status = false;
      },
    },
  };
</script>