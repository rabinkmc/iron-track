// src/plugins/axios.js
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api", // ⬅️ Replace with your backend API base
  timeout: 10000,
});

export default {
  install: (app) => {
    app.config.globalProperties.$axios = api;
    app.provide("axios", api); // optional if you want to use inject() too
  },
};

export { api }; // export instance for direct import if needed
