import "./assets/main.css";

import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";

import router from "@/router";
import config from "@/config";
import store from "@/stores";

const app = createApp(App);

app.provide("config", config);
app.use(createPinia());
app.use(router);
app.use(store);

app.mount("#app");
