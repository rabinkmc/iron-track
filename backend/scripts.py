# create a standalone script
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

push_exercises = [
    {
        "name": "Barbell Bench Press",
        "muscle_targeted": "Chest",
        "description": "A compound lift targeting the chest, shoulders, and triceps using a barbell.",
    },
    {
        "name": "Incline Dumbbell Press",
        "muscle_targeted": "Upper Chest",
        "description": "Targets the upper chest using dumbbells on an incline bench.",
    },
    {
        "name": "Dumbbell Shoulder Press",
        "muscle_targeted": "Shoulders",
        "description": "Overhead press focusing on the deltoids using dumbbells.",
    },
    {
        "name": "Lateral Raises",
        "muscle_targeted": "Side Delts",
        "description": "Isolation movement to build the lateral deltoids.",
    },
    {
        "name": "Machine Chest Press",
        "muscle_targeted": "Chest",
        "description": "Chest-focused pressing movement using a machine for stability.",
    },
    {
        "name": "Machine Shoulder Press",
        "muscle_targeted": "Shoulders",
        "description": "Overhead pressing machine emphasizing shoulder muscles.",
    },
    {
        "name": "Triceps Pushdown",
        "muscle_targeted": "Triceps",
        "description": "Cable-based movement that isolates the triceps.",
    },
    {
        "name": "Overhead Triceps Extension",
        "muscle_targeted": "Triceps",
        "description": "Extension movement performed overhead to target long triceps head.",
    },
    {
        "name": "Cable Chest Fly",
        "muscle_targeted": "Chest",
        "description": "Cable-based fly movement for chest contraction and shaping.",
    },
    {
        "name": "Close Grip Bench Press",
        "muscle_targeted": "Triceps",
        "description": "Barbell press variation that targets the triceps more than chest.",
    },
]

pull_exercises = [
    {
        "name": "Deadlift",
        "muscle_targeted": "Back",
        "description": "Full-body compound lift emphasizing posterior chain and back.",
    },
    {
        "name": "Pull-ups",
        "muscle_targeted": "Lats",
        "description": "Bodyweight movement primarily working the latissimus dorsi.",
    },
    {
        "name": "Barbell Row",
        "muscle_targeted": "Mid Back",
        "description": "Horizontal pulling movement using a barbell to build thickness.",
    },
    {
        "name": "Lat Pulldown",
        "muscle_targeted": "Lats",
        "description": "Vertical pulling machine mimicking pull-ups.",
    },
    {
        "name": "Seated Cable Row",
        "muscle_targeted": "Back",
        "description": "Cable-based horizontal pulling exercise targeting mid-back.",
    },
    {
        "name": "Face Pulls",
        "muscle_targeted": "Rear Delts",
        "description": "Cable movement focused on rear deltoids and upper back.",
    },
    {
        "name": "EZ Bar Curl",
        "muscle_targeted": "Biceps",
        "description": "Barbell curl variation with ergonomic grip for biceps.",
    },
    {
        "name": "Hammer Curls",
        "muscle_targeted": "Biceps and Forearms",
        "description": "Dumbbell curls with neutral grip to target brachialis and forearms.",
    },
    {
        "name": "Concentration Curl",
        "muscle_targeted": "Biceps",
        "description": "Isolated curl focusing on peak contraction of biceps.",
    },
    {
        "name": "Cable Curl",
        "muscle_targeted": "Biceps",
        "description": "Constant tension curl using a cable machine.",
    },
]

leg_exercises = [
    {
        "name": "Barbell Back Squat",
        "muscle_targeted": "Quads and Glutes",
        "description": "Compound movement for lower body strength and size.",
    },
    {
        "name": "Romanian Deadlift",
        "muscle_targeted": "Hamstrings and Glutes",
        "description": "Hip hinge movement targeting the hamstrings and glutes.",
    },
    {
        "name": "Leg Press",
        "muscle_targeted": "Quads",
        "description": "Machine-based lower body pressing movement emphasizing the quads.",
    },
    {
        "name": "Lunges",
        "muscle_targeted": "Quads and Glutes",
        "description": "Single-leg movement to improve balance and leg development.",
    },
    {
        "name": "Leg Curl Machine",
        "muscle_targeted": "Hamstrings",
        "description": "Isolated hamstring movement using a machine.",
    },
    {
        "name": "Leg Extension Machine",
        "muscle_targeted": "Quads",
        "description": "Machine movement to isolate and develop quadriceps.",
    },
    {
        "name": "Glute Bridge",
        "muscle_targeted": "Glutes",
        "description": "Bodyweight or weighted bridge movement to activate glutes.",
    },
    {
        "name": "Bulgarian Split Squat",
        "muscle_targeted": "Quads and Glutes",
        "description": "Single-leg squat variation emphasizing leg strength and stability.",
    },
    {
        "name": "Seated Calf Raise",
        "muscle_targeted": "Calves",
        "description": "Calf isolation exercise with emphasis on soleus muscle.",
    },
    {
        "name": "Standing Calf Raise",
        "muscle_targeted": "Calves",
        "description": "Targets the gastrocnemius muscle through ankle extension.",
    },
]

from iron.models import Exercise

for ex in push_exercises + pull_exercises + leg_exercises:
    Exercise.objects.create(**ex)
