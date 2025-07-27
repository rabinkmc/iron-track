import { createRouter, createWebHistory } from "vue-router";

import HomePage from "../pages/HomePage.vue";
import LoginPage from "../pages/LoginPage.vue";
import WorkoutSession from "../pages/WorkoutSession.vue";
import WorkoutSessionDetail from "../components/WorkoutSessionDetail.vue";
import ExercisePage from "../pages/ExercisePage.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomePage,
    meta: { requiresAuth: true },
  },
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
];

const router = createRouter({
  history: createWebHistory(import.meta.env.VITE_BASE_URL),
  routes,
});

router.beforeEach((to, _, next) => {
  const isAuthenticated = !!localStorage.getItem("access_token");

  if (to.name !== "login" && !isAuthenticated) {
    next({ name: "login" });
  } else if (to.name === "login" && isAuthenticated) {
    next({ name: "home" });
  } else {
    next();
  }
});

export default router;
