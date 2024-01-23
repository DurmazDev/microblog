import "./assets/main.css";
import "vue-toastify/index.css";

import * as Vue from "vue";
import { createPinia } from "pinia";
import plugin from "vue-toastify";

import App from "./App.vue";

import router from "@/router";
import config from "@/config";
import store from "@/stores";

import VueAxios from "vue-axios";
import { InitApiService } from "./services/api.service";

const app = Vue.createApp(App);
const api = InitApiService(config.apiUrl);
app.use(VueAxios, api);

app.provide("config", config);
app.use(createPinia());
app.use(plugin, {
  errorDuration: 3000,
  warningInfoDuration: 3000,
  successDuration: 3000,
});

router.beforeEach((to, from, next) => {
  if (
    config.PROTECTED_ROUTES.includes(to.path) &&
    !store.getters.isAuthenticated
  ) {
    router.push({ name: "login" });
  } else {
    next();
  }
});

app.use(router);
app.use(store);

app.mount("#app");
