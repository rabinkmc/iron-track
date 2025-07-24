<template>
  <v-container>
    <v-data-table
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
  </v-container>
</template>

<script setup>
import { ref, inject, onMounted } from "vue";
import { useRoute } from "vue-router";

const axios = inject("axios");
const route = useRoute();
const apiUrl = `/iron/session/${route.params.id}`;

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
</script>

<style scoped>
td {
  padding: 8px 12px;
  text-align: center;
}
</style>
