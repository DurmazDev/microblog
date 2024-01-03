import ApiService from "@/core/services/api.service";
import JwtService from "@/core/services/jwt.service";

const state = {
  errors: null,
  user: null,
  isAuthenticated: !!JwtService.getToken(),
};

const getters = {
  currentUser(state) {
    return state.user;
  },
  currentUserInfo(state) {
    return state.user_info;
  },
  isAuthenticated(state) {
    return state.isAuthenticated;
  },
};

const mutations = {
  [SET_ERROR](state, error) {
    state.errors = error;
  },
  [SET_AUTH](state, user) {
    state.isAuthenticated = true;
    state.errors = {};
    state.user = user;
    JwtService.saveToken(user.token);
  },
  [SET_PASSWORD](state, password) {
    state.user.password = password;
  },
  [SET_EMAIL](state, email) {
    state.user.email = email;
  },
  [SET_PASSWORD](state, password) {
    state.user.password = password;
  },
  [PURGE_AUTH](state) {
    state.isAuthenticated = false;
    state.user = {};
    JwtService.destroyToken();
    axios.defaults.headers.common["Authorization"] = null;
  },
};

const actions = {
  [LOGIN](context, credentials) {
    return new Promise((resolve, reject) => {
      const bodyFormData = {
        email: credentials.email,
        password: credentials.password,
      };
      axios({
        method: "post",
        url: "login",
        data: JSON.stringify(bodyFormData),
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      })
        .then((response) => {
          context.commit(SET_AUTH, response.data.data);
          context.commit(SET_PASSWORD, credentials.password);
          context.commit(SET_EMAIL, credentials.email);
          resolve(response);
        })
        .catch(() => {
          context.commit(SET_ERROR, "Kullanıcı adı veya şifre hatalı");
          reject("Kullanıcı adı veya şifre hatalı");
        });
    });
  },
  [REGISTER](context, credentials) {
    return new Promise((resolve, reject) => {
      const name = credentials.name;
      const surname = credentials.surname;
      const username = credentials.username;
      const email = credentials.email;
      const password = credentials.password;

      const bodyFormData = {
        name: name,
        surname: surname,
        username: username,
        email: email,
        password: password,
      };
      axios({
        method: "post",
        url: "register",
        data: JSON.stringify(bodyFormData),
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      })
        .then((response) => {
          resolve(response);
          context.commit(SET_AUTH, response.data.result);
          context.commit(SET_PASSWORD, credentials.password);
          context.commit(SET_EMAIL, credentials.email);
        })
        .catch((err) => {
          reject(err);
        });
    });
  },
  [LOGOUT](context) {
    context.commit(PURGE_AUTH);
  },
  [VERIFY_AUTH](context) {
    if (JwtService.getToken()) {
      ApiService.setHeader();
    } else {
      context.commit(PURGE_AUTH);
    }
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
