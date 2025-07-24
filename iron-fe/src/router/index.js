// src/router/index.ts

import { createRouter, createWebHistory } from "vue-router";

import HomePage from "@/views/HomePage.vue";
import LoginPage from "@/views/LoginPage.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomePage,
    meta: { requiresAuth: true },
  },
  {
    path: "/login",
    name: "login",
    component: LoginPage,
    meta: { guestOnly: true },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

isAuthenticated = () => {
  return !!localStorage.getItem("access_token");
};

router.beforeEach((to, from, next) => {
  const loggedIn = isAuthenticated();

  if (to.meta.requiresAuth && !loggedIn) {
    return next({ name: "login" });
  }

  if (to.meta.guestOnly && loggedIn) {
    return next({ name: "home" });
  }

  return next();
});

export default router;
