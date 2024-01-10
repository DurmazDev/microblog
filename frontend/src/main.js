import "./assets/main.css";

import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";

import router from "@/router";
import config from "@/config";
import store from "@/stores";
import { InitApiService } from "./services/api.service";

const app = createApp(App);

app.provide("config", config);
app.use(createPinia());

router.beforeEach((to, from, next) => {
  if (config.PUBLIC_ROUTES.includes(to.name)) {
    next();
  } else if (!store.getters.isAuthenticated) {
    router.push({ name: "login" });
  } else {
    next();
  }
});

app.use(router);
app.use(store);

InitApiService(config.apiUrl);

app.mount("#app");
