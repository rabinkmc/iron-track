<template>
  <v-container>
    <v-app-bar app>
      <v-toolbar-title>Workout Session</v-toolbar-title>
      <v-spacer />
      <v-btn icon @click="onEdit">
        <v-icon>mdi-pencil</v-icon>
      </v-btn>
      <v-btn icon @click="deleteSession">
        <v-icon>mdi-delete</v-icon>
      </v-btn>
    </v-app-bar>
    <v-data-table
      v-if="!enableEdit"
      :items="tableItems"
      class="elevation-1"
      disable-pagination
      hide-default-footer
    >
      <template #item="{ item }">
        <tr>
          <td>{{ item.sn }}</td>
          <td>{{ item.exercise }}</td>
          <td v-for="n in maxSets" :key="n">
            <div v-if="item.sets[n - 1]">
              {{ item.sets[n - 1].reps }} / {{ item.sets[n - 1].weight }}
            </div>
          </td>
        </tr>
      </template>
    </v-data-table>
    <WorkoutSessionEdit
      v-else
      :form="sessionData"
      @submit="onSubmit"
    ></WorkoutSessionEdit>
  </v-container>
</template>

<script setup>
import { ref, inject, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import WorkoutSessionEdit from "./WorkoutSessionEdit.vue";

const axios = inject("axios");
const route = useRoute();
const apiUrl = `/iron/session/${route.params.id}/`;
const enableEdit = ref(false);
const router = useRouter();

const sessionData = ref(null);
const maxSets = 5;

const headers = [
  { text: "SN", value: "sn", width: "50px" },
  { text: "Exercise", value: "exercise" },
  ...Array.from({ length: maxSets }, (_, i) => ({
    text: `Set ${i + 1}`,
    value: `set${i + 1}`,
  })),
];

// Process API data into table format
const tableItems = ref([]);

function processData(data) {
  return data.session_exercises.map((ex, index) => ({
    sn: index + 1,
    exercise: ex.exercise.name,
    sets: ex.sets.slice(0, maxSets).map((set) => ({
      reps: set.reps,
      weight: set.weight,
    })),
  }));
}

function onEdit() {
  enableEdit.value = !enableEdit.value;
}

function onSubmit(session) {
  sessionData.value = session;
  enableEdit.value = false;
  tableItems.value = processData(sessionData.value);
}

// On mounted, fetch data from API
onMounted(async () => {
  try {
    const response = await axios.get(apiUrl);
    sessionData.value = response.data;
    tableItems.value = processData(sessionData.value);
  } catch (error) {
    console.error("Error fetching workout session:", error);
  }
});
async function deleteSession() {
  if (confirm("Are you sure you want to delete this session?")) {
    try {
      await axios.delete(apiUrl);
      router.push({ name: "home" }); // Replace "home" with your desired route
    } catch (error) {
      console.error("Failed to delete session:", error);
      alert("Failed to delete session.");
    }
  }
}
</script>

<style scoped>
td {
  padding: 8px 12px;
  text-align: center;
}
</style>
