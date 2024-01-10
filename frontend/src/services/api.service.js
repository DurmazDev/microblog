import axios from "axios";
import jwtService from "@/services/jwt.service";

const api = axios.create({
  headers: {
    "Content-Type": "application/json",
  },
});

const InitApiService = (apiUrl) => {
  api.defaults.baseURL = apiUrl;
  api.interceptors.request.use(
    (config) => {
      const token = jwtService.getToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );
};

export { InitApiService, api };
