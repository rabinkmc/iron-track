import { createRouter, createWebHistory } from "vue-router";

import HomePage from "../pages/HomePage.vue";
import LoginPage from "../pages/LoginPage.vue";
import SignUpPage from "../pages/SignUpPage.vue";
import WorkoutSession from "../pages/WorkoutSession.vue";
import WorkoutSessionDetail from "../components/WorkoutSessionDetail.vue";
import ExercisePage from "../pages/ExercisePage.vue";

const routes = [
  {
    path: "/workout-session/add",
    name: "workout-create",
    component: WorkoutSession,
    meta: { requiresAuth: true },
  },
  {
    path: "/workout-session/:id",
    name: "workout-session-detail",
    component: WorkoutSessionDetail,
  },
  {
    path: "/exercise",
    name: "exercise",
    component: ExercisePage,
  },
  {
    path: "/login",
    name: "login",
    component: LoginPage,
    meta: { guestOnly: true },
  },
  {
    path: "/signup",
    name: "signup",
    component: SignUpPage,
    meta: { guestOnly: true },
  },
  {
    path: "/",
    name: "home",
    component: HomePage,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.VITE_BASE_URL),
  routes,
});

router.beforeEach((to, _, next) => {
  const isAuthenticated = !!localStorage.getItem("access_token");

  if (to.meta.requiresAuth && !isAuthenticated) {
    return next({ name: "login" });
  }

  if (to.meta.guestOnly) {
    if (isAuthenticated) {
      return next({ name: "home" });
    }
    if (to.name === "signup") {
      return next();
    }
  }

  next();
});

export default router;
