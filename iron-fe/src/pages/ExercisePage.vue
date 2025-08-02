<template>
  <v-container>
    <v-toolbar flat>
      <v-toolbar-title>Exercises</v-toolbar-title>
      <v-spacer />
      <v-btn color="primary" @click="openCreateDialog">New Exercise</v-btn>
    </v-toolbar>

    <!-- Exercise Table -->
    <v-data-table-server
      :headers="headers"
      :items="exercises"
      :options.sync="options"
      :server-items-length="count"
      :loading="loading"
      :items-length="exercises.length"
      @update:options="onUpdateOptions"
      class="mt-4"
    >
      <template #item.description="{ item }">
        <div
          style="
            max-width: 300px;
            /*white-space: nowrap;*/
            overflow: hidden;
            text-overflow: ellipsis;
          "
        >
          {{ item.description }}
        </div>
      </template>
      <template #item.actions="{ item }">
        <v-btn small icon @click="openEditDialog(item)">
          <v-icon>mdi-pencil</v-icon>
        </v-btn>
        <v-btn icon @click="openDeleteDialog(item)">
          <v-icon>mdi-delete</v-icon>
        </v-btn>
      </template>
    </v-data-table-server>

    <!-- Create/Edit Dialog -->
    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title
          >{{ isEditMode ? "Edit" : "Create" }} Exercise</v-card-title
        >
        <v-card-text>
          <v-text-field v-model="form.name" label="Name" />
          <v-text-field
            v-model="form.muscle_targeted"
            label="Muscle Targeted"
          />
          <v-textarea v-model="form.description" label="Description" rows="3" />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="dialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="saveExercise">{{
            isEditMode ? "Update" : "Create"
          }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h6">Confirm Delete</v-card-title>
        <v-card-text
          >Are you sure you want to delete "{{ selected?.name }}"?</v-card-text
        >
        <v-card-actions>
          <v-spacer />
          <v-btn @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="error" @click="deleteExercise">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted, watch, inject } from "vue";

const axios = inject("axios");

const exercises = ref([]);
const count = ref(0);
const loading = ref(false);

const headers = [
  { title: "id", key: "id" },
  { title: "Name", key: "name" },
  { title: "Muscle Targeted", key: "muscle_targeted" },
  { title: "Description", key: "description" },
  { title: "Actions", key: "actions", sortable: false },
];

const dialog = ref(false);
const deleteDialog = ref(false);
const isEditMode = ref(false);

const form = ref({
  name: "",
  muscle_targeted: "",
  description: "",
});

const selected = ref(null);
const options = ref({
  page: 1,
  itemsPerPage: 10,
  sortBy: [],
  sortDesc: [],
});

const fetchExercises = async () => {
  const { page } = options.value;
  loading.value = true;
  const res = await axios.get("/iron/exercise/", {
    params: {
      page,
    },
  });
  exercises.value = res.data.results;
  count.value = res.data.count;
  loading.value = false;
};

const openCreateDialog = () => {
  isEditMode.value = false;
  form.value = { name: "", muscle_targeted: "", description: "" };
  dialog.value = true;
};

const openEditDialog = (exercise) => {
  isEditMode.value = true;
  selected.value = exercise;
  form.value = { ...exercise };
  dialog.value = true;
};

const openDeleteDialog = (exercise) => {
  selected.value = exercise;
  deleteDialog.value = true;
};

const saveExercise = async () => {
  try {
    if (isEditMode.value) {
      await axios.put(`/iron/exercise/${selected.value.id}/`, form.value);
    } else {
      await axios.post("iron/exercise/", form.value);
    }
    dialog.value = false;
    await fetchExercises();
  } catch (error) {
    console.error("Error saving exercise:", error);
  }
};

const deleteExercise = async () => {
  try {
    await axios.delete(`/iron/exercise/${selected.value.id}/`);
    deleteDialog.value = false;
    await fetchExercises();
  } catch (error) {
    console.error("Error deleting exercise:", error);
  }
};

watch(options, fetchExercises, { deep: true });
const onUpdateOptions = (newOptions) => {
  options.value = newOptions;
};
onMounted(async () => {
  await fetchExercises();
});
</script>
