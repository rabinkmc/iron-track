<template>
  <v-container class="py-6">
    <v-row>
      <v-col cols="12">
        <v-card class="pa-4" outlined>
          <v-card-title class="text-h5">New Workout Session</v-card-title>

          <v-form @submit.prevent="submitSession">
            <v-text-field
              v-model="form.date"
              label="Date"
              type="date"
              required
            />

            <v-textarea v-model="form.notes" label="Session Notes" rows="2" />
            <v-divider class="my-4" />
            <v-card-subtitle>Exercises</v-card-subtitle>
            <div
              v-for="(exerciseEntry, index) in form.session_exercises"
              :key="index"
              class="mb-6"
            >
              <v-select
                v-model="exerciseEntry.exercise"
                :items="exerciseOptions"
                item-title="name"
                item-value="id"
                label="Exercise"
                required
              />

              <v-textarea
                v-model="exerciseEntry.notes"
                label="Exercise Notes"
                rows="1"
              />

              <v-card-subtitle class="mt-2">Sets</v-card-subtitle>
              <v-row
                v-for="(set, setIndex) in exerciseEntry.sets"
                :key="setIndex"
              >
                <v-col cols="5">
                  <v-text-field
                    v-model.number="set.reps"
                    label="Reps"
                    type="number"
                    min="1"
                    required
                  />
                </v-col>
                <v-col cols="5">
                  <v-text-field
                    v-model.number="set.weight"
                    label="Weight (kg)"
                    type="number"
                    min="0"
                    step="0.1"
                    required
                  />
                </v-col>
                <v-col cols="2" class="d-flex align-center">
                  <v-btn icon @click="removeSet(index, setIndex)"
                    ><v-icon>mdi-delete</v-icon></v-btn
                  >
                </v-col>
              </v-row>

              <v-btn
                size="small"
                class="mt-1"
                @click="addSet(index)"
                variant="text"
              >
                + Add Set
              </v-btn>

              <v-divider class="my-4" />
            </div>

            <v-btn color="secondary" @click="addExercise">
              + Add Exercise
            </v-btn>

            <v-divider class="my-4" />

            <v-btn color="primary" type="Submit">Save Session</v-btn>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { inject } from "vue";

const axios = inject("axios");
const router = useRouter();

const form = ref({
  user: localStorage.getItem("user_id"),
  date: new Date().toISOString().slice(0, 10),
  notes: "",
  session_exercises: [],
});

const exerciseOptions = ref([]);

const fetchExercises = async () => {
  try {
    const response = await axios.get("/iron/exercise/");
    exerciseOptions.value = response.data.results;
  } catch (error) {
    console.error("Failed to fetch exercises", error);
  }
};

onMounted(() => {
  fetchExercises();
});

const addExercise = () => {
  form.value.session_exercises.push({
    exercise: null,
    notes: "",
    sets: [{ reps: 10, weight: 0 }],
  });
};

const removeSet = (exerciseIndex, setIndex) => {
  form.value.session_exercises[exerciseIndex].sets.splice(setIndex, 1);
};

const addSet = (exerciseIndex) => {
  form.value.session_exercises[exerciseIndex].sets.push({
    reps: 10,
    weight: 0,
  });
};

const submitSession = async () => {
  try {
    const sessionRes = await axios.post(
      "/iron/session/bulk-create/",
      form.value,
    );

    router.push({ name: "home" });
  } catch (error) {
    console.error("Failed to submit workout session", error);
  }
};
</script>
