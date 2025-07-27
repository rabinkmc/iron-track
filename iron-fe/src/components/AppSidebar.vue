<template>
  <v-navigation-drawer app permanent>
    <v-list-item class="px-4" link :to="{ name: 'home' }">
      <v-icon>mdi-dumbbell</v-icon>
      <span class="ml-2 font-weight-bold text-h6">Iron Track</span>
    </v-list-item>

    <v-divider></v-divider>

    <v-list nav dense>
      <v-list-item
        v-for="item in navItems"
        :key="item.title"
        :to="{ name: item.routeName }"
        link
      >
        <v-icon>{{ item.icon }}</v-icon>
        <v-list-item-title>{{ item.title }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script setup>
const navItems = [
  { title: "Dashboard", icon: "mdi-view-dashboard", routeName: "home" },
  { title: "Exercises", icon: "mdi-run", routeName: "exercise" },
];
</script>
