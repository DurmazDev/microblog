import JwtService from "@/services/jwt.service";
import { api } from "@/services/api.service";

export const LOGIN = "login";
export const REGISTER = "register";
export const LOGOUT = "logout";
export const SET_AUTH = "setAuth";
export const SET_ERROR = "setError";
export const SET_USER = "setUser";
export const UNSET_AUTH = "unsetAuth";

const state = {
  errors: null,
  user: null,
  isAuthenticated: !!JwtService.getToken(),
};

const getters = {
  currentUser(state) {
    return state.user;
  },
  isAuthenticated(state) {
    return state.isAuthenticated;
  },
  errorMessages(state) {
    return state.errors;
  },
};

const mutations = {
  [SET_ERROR](state, error) {
    state.errors = error;
  },
  [SET_AUTH](state, auth_data) {
    state.isAuthenticated = true;
    state.errors = {};
    state.user = auth_data.user;
    JwtService.saveToken(auth_data.token);
  },
  [SET_USER](state, user) {
    state.user = user;
  },
  [UNSET_AUTH](state) {
    state.isAuthenticated = false;
    state.user = {};
    JwtService.removeToken();
    api.defaults.headers.common["Authorization"] = null;
  },
};

const actions = {
  login(store, credentials) {
    const body = {
      email: credentials.email,
      password: credentials.password,
    };
    return new Promise((resolve, reject) => {
      api({
        method: "POST",
        url: "auth/login",
        data: JSON.stringify(body),
      })
        .then((response) => {
          console.log(response.data.token);
          store.commit("setAuth", {
            user: response.data.user,
            token: response.data.token,
          });
          resolve(response);
        })
        .catch((err) => {
          let error_message = err.response.data.error;
          store.commit(
            "setError",
            error_message ? error_message : "Something went wrong"
          );
          reject(err);
        });
    });
  },
  register(store, credentials) {
    const body = {
      name: credentials.name,
      email: credentials.email,
      password: credentials.password,
    };
    return new Promise((resolve, reject) => {
      api({
        method: "POST",
        url: "auth/register",
        data: JSON.stringify(body),
      })
        .then((response) => {
          store.commit("setAuth", response.data.user, response.data.token);
          resolve(response);
        })
        .catch((err) => {
          store.commit("setError", err);
          reject(err);
        });
    });
  },
  logout(store) {
    return new Promise((resolve, reject) => {
      store.commit("unsetAuth");
      api({
        method: "DELETE",
        url: "auth/logout",
      })
        .then((response) => {
          resolve(response);
        })
        .catch((err) => {
          store.commit("setError", err);
          reject(err);
        });
    });
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
