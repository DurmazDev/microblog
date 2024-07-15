import Vuex from "vuex";
import config from "@/config.js";

import moduleAuth from "../stores/auth.module";
import createPersistedState from "vuex-persistedstate";

const store = new Vuex.Store({
  plugins: [
    createPersistedState({
      key: "vuex",
    }),
  ],
  modules: {
    auth: moduleAuth,
  },
  strict: config.devMode,
});

export default store;
