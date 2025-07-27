<template>
  <v-app>
    <AppSidebar v-if="showLayout" />
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { useRoute } from "vue-router";
import { computed } from "vue";
const route = useRoute();
const showLayout = computed(() => route.name !== "login");
</script>
