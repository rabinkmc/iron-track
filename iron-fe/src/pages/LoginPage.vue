<template>
  <v-container fluid class="fill-height pa-0">
    <v-row no-gutters>
      <!-- Left side with image -->
      <v-col cols="12" md="6" class="image-col d-none d-md-flex">
        <v-img
          src="https://i.pinimg.com/1200x/ca/4d/1c/ca4d1ca44a867adb45e8b220e3ebb5e9.jpg"
          cover
          class="w-100 h-100"
        ></v-img>
      </v-col>

      <!-- Right side with login form -->
      <v-col
        cols="12"
        md="6"
        class="d-flex align-center justify-center pa-8 bg-white"
      >
        <v-card width="100%" max-width="400" class="pa-6 elevation-10">
          <v-card-title class="text-h5 text-center mb-4">
            Welcome to Iron Track
          </v-card-title>

          <v-form @submit.prevent="handleLogin" ref="loginForm">
            <v-text-field
              v-model="username"
              label="Username"
              prepend-inner-icon="mdi-account"
              required
            ></v-text-field>

            <v-text-field
              v-model="password"
              label="Password"
              type="password"
              prepend-inner-icon="mdi-lock"
              required
            ></v-text-field>

            <v-btn type="submit" color="primary" block class="mt-4">
              Login
            </v-btn>

            <div class="mt-4 text-center">
              <small>Don’t have an account? <a href="#">Sign up</a></small>
            </div>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import { inject } from "vue";
import { useRouter } from "vue-router";

const axios = inject("axios");
const username = ref("");
const password = ref("");
const loginForm = ref(null);
const router = useRouter();
const handleLogin = async () => {
  const response = await axios.post("/token/", {
    username: username.value,
    password: password.value,
  });
  localStorage.setItem("access_token", response.data.access);
  localStorage.setItem("refresh_token", response.data.refresh);
  router.push({ name: "home" });
};
</script>

<style scoped>
.image-col {
  background-color: #000;
}
</style>
