// src/plugins/axios.js
import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      // Optionally, you can implement a refresh token logic here
      // For example, check if a refresh token is available and use it to get a new access token

      const refreshToken = localStorage.getItem("refresh_token");
      if (refreshToken) {
        try {
          const response = await axios.post(
            `${import.meta.env.VITE_API_URL}/token/refresh`,
            { refresh_token: refreshToken },
          );
          const { access_token } = response.data;
          localStorage.setItem("access_token", access_token);
          api.defaults.headers.common["Authorization"] =
            `Bearer ${access_token}`;
          originalRequest.headers["Authorization"] = `Bearer ${access_token}`;
          return api(originalRequest);
        } catch (refreshError) {
          // redirect to login if refresh fails
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          localStorage.removeItem("user_id");
          window.location.href = "/login"; // or use router to navigate
        }
      }
    }

    return Promise.reject(error);
  },
);

export default {
  install: (app) => {
    app.provide("axios", api); // optional if you want to use inject() too
  },
};

export { api }; // export instance for direct import if needed
