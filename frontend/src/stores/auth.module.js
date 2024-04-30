import JwtService from "@/services/jwt.service";
import config from "@/config";
import { InitApiService } from "@/services/api.service";

export const LOGIN = "login";
export const VERIFY_2FA = "verify2FA";
export const SET_2FA_STATUS = "set2FAStatus";
export const REGISTER = "register";
export const LOGOUT = "logout";
export const SET_AUTH = "setAuth";
export const SET_ERROR = "setError";
export const SET_USER = "setUser";
export const UNSET_AUTH = "unsetAuth";

// WARN(ahmet): This is a workaround for the circular dependency issue.
const api = InitApiService(config.apiUrl);

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
  is2FAEnabled(state) {
    return state.user && state.user.is_2fa_enabled;
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
    state.errors = {};
    state.user = auth_data.user;
    JwtService.saveToken(auth_data.token);
    state.isAuthenticated = true;
  },
  [SET_USER](state, user) {
    state.user = user;
  },
  [UNSET_AUTH](state) {
    state.user = {};
    JwtService.removeToken();
    state.isAuthenticated = false;
  },
};

const actions = {
  set2FAStatus(store, status) {
    store.commit("setUser", {
      ...store.state.user,
      is_2fa_enabled: status,
    });
  },
  verify2FA(store, verificationCode) {
    return new Promise((resolve, reject) => {
      api({
        method: "POST",
        url: "auth/verify-2fa/" + verificationCode,
        headers: {
          Authorization: `Bearer ${JwtService.getToken()}`,
        },
      })
        .then((response) => {
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
          store.commit("setAuth", {
            user: response.data.user,
            token: response.data.token,
          });
          resolve(response);
        })
        .catch((err) => {
          if (err.response.status === 302) {
            state.errors = {};
            JwtService.saveToken(err.response.data.token);
            resolve(err.response);
            return;
          }
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
          store.commit("setAuth", {
            user: response.data.user,
            token: response.data.token,
          });
          resolve(response);
        })
        .catch((err) => {
          store.commit("setError", err.response.data.error);
          reject(err);
        });
    });
  },
  logout(store) {
    return new Promise((resolve, reject) => {
      api({
        method: "DELETE",
        url: "auth/logout",
        headers: {
          Authorization: `Bearer ${JwtService.getToken()}`,
        },
      })
        .then((response) => {
          store.commit("unsetAuth");
          resolve(response);
        })
        .catch((err) => {
          store.commit("unsetAuth");
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
