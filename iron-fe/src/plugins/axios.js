// src/plugins/axios.js
import axios from "axios";

// import API URL from environment variables
const api = axios.create({
  baseURL: import.meta.env.API_URL || "http://localhost:8000/api",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

// console log api base url

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

export default {
  install: (app) => {
    app.provide("axios", api); // optional if you want to use inject() too
  },
};

export { api }; // export instance for direct import if needed
