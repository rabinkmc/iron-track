<template>
  <v-container class="pa-6" max-width="1200">
    <v-row align="center" justify="space-between" class="mb-6">
      <v-btn @click="beginWorkout"> Begin Workout Session </v-btn>
      <v-btn color="error" variant="outlined" @click="logout"> Logout </v-btn>
    </v-row>

    <v-row>
      <v-col cols="12" md="8">
        <v-row dense>
          <v-col v-for="session in sessions" :key="session.id" cols="12" md="6">
            <v-card outlined class="pa-4" @click="loadSession(session)">
              <v-card-title class="headline">
                Workout Session {{ formatDate(session.date) }}
              </v-card-title>
              <v-card-subtitle class="mb-3">
                {{ session.notes || "No notes" }}
              </v-card-subtitle>

              <v-chip-group column>
                <v-chip
                  v-for="exercise in session.session_exercises"
                  :key="exercise.exercise.id"
                  class="ma-1"
                  color="secondary"
                  variant="outlined"
                  small
                >
                  {{ exercise.exercise.name }}
                </v-chip>
              </v-chip-group>
            </v-card>
          </v-col>
        </v-row>
      </v-col>

      <!-- Progress Card -->
      <v-col cols="12" md="4">
        <v-card class="pa-4" outlined>
          <v-card-title class="headline">Weekly Progress</v-card-title>
          <v-card-subtitle class="mb-3">
            Sessions completed this week
          </v-card-subtitle>

          <v-row>
            <v-col
              v-for="(day, i) in weekData"
              :key="i"
              class="text-center"
              cols="3"
            >
              <div class="text-caption">{{ day.day }}</div>
              <v-icon :color="day.completed ? 'green' : 'grey'">
                mdi-check-circle
              </v-icon>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>

    <!-- Loading Dialog -->
    <v-dialog v-model="loading" persistent width="300">
      <v-card>
        <v-card-text class="text-center">
          Loading...
          <v-progress-circular
            indeterminate
            color="primary"
            class="mt-4"
          ></v-progress-circular>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { inject } from "vue";

const router = useRouter();
const axios = inject("axios");

const sessions = ref([]);
const loading = ref(false);

// Mock weekly data
const weekData = ref([
  { day: "Mon", completed: true },
  { day: "Tue", completed: false },
  { day: "Wed", completed: true },
  { day: "Thu", completed: true },
  { day: "Fri", completed: false },
  { day: "Sat", completed: true },
  { day: "Sun", completed: false },
]);

const fetchSessions = async () => {
  loading.value = true;
  try {
    const response = await axios.get("/iron/session/");
    sessions.value = response.data;
  } catch (error) {
    console.error("Failed to load sessions", error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchSessions();
});

const beginWorkout = () => {
  router.push({ name: "workout-create" });
};

const loadSession = (session) => {
  router.push({ name: "workout-session-detail", params: { id: session.id } });
};

const logout = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  router.push({ name: "login" });
};

const formatDate = (dateStr) => {
  const d = new Date(dateStr);
  return d.toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
};
</script>
