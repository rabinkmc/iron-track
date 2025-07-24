import { createRouter, createWebHistory } from "vue-router";

import HomePage from "../pages/HomePage.vue";
import LoginPage from "../pages/LoginPage.vue";
import WorkoutSession from "../pages/WorkoutSession.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomePage,
    meta: { requiresAuth: true },
  },
  {
    path: "/workout-session",
    name: "workout-session",
    component: WorkoutSession,
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

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem("access_token");

  if (to.name !== "login" && !isAuthenticated) {
    next({ name: "login" });
  } else if (to.name === "login" && isAuthenticated) {
    next({ name: "home" }); // optional: redirect logged-in user away from login
  } else {
    next();
  }
});

export default router;
