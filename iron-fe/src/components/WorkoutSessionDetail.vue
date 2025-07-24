<template>
  <div class="max-w-4xl mx-auto p-4 space-y-6" v-if="session">
    <div class="bg-white shadow-md rounded-xl p-6 border border-gray-100">
      <h1 class="text-2xl font-bold mb-2">Workout Session</h1>
      <p class="text-gray-600">📅 {{ session.date }}</p>
      <p class="text-gray-800 mt-2 whitespace-pre-line">{{ session.notes }}</p>
    </div>

    <div
      v-for="(entry, index) in session.session_exercises"
      :key="index"
      class="bg-white shadow-sm rounded-xl p-4 border border-gray-200"
    >
      <div class="flex justify-between items-start mb-2">
        <div>
          <h2 class="text-xl font-semibold capitalize">
            {{ entry.exercise.name }}
          </h2>
          <p class="text-sm text-gray-500">
            💪 {{ entry.exercise.muscle_targeted }}
          </p>
        </div>
      </div>

      <p v-if="entry.notes" class="text-gray-700 italic mt-1">
        📝 {{ entry.notes }}
      </p>

      <table
        class="w-full mt-4 border border-gray-200 rounded-lg overflow-hidden text-sm"
      >
        <thead class="bg-gray-100 text-left">
          <tr>
            <th class="p-2">Set</th>
            <th class="p-2">Reps</th>
            <th class="p-2">Weight (kg)</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(set, setIndex) in entry.sets"
            :key="set.id"
            class="border-t"
          >
            <td class="p-2">{{ setIndex + 1 }}</td>
            <td class="p-2">{{ set.reps }}</td>
            <td class="p-2">{{ set.weight }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div v-else class="text-center py-10">
    <p>Loading workout session...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { inject } from "vue";

const axios = inject("axios");

const session = ref(null);

const fetchSession = async () => {
  try {
    const response = await axios.get("/iron/session/1/");
    session.value = response.data;
  } catch (error) {
    console.error("Failed to fetch session data:", error);
  }
};

onMounted(() => {
  fetchSession();
});
</script>
