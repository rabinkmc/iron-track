from iron.models import (
    WorkoutSession,
    WorkoutSessionExercise,
    WorkoutSessionExerciseSet,
)


def update_exercise(exercise, data):
    exercise.name = data["name"]
    exercise.muscle_targeted = data["muscle_targeted"]
    exercise.description = data.get("description", "")
    exercise.save()


def create_workout_session(data):
    user = data["user"]
    workout_date = data.get("date")
    notes = data.get("notes", "")
    workout_session = WorkoutSession.objects.create(
        user=user,
        date=workout_date,
        notes=notes,
    )
    for session_exercise_data in data.get("session_exercises", []):
        session_exercise = WorkoutSessionExercise.objects.create(
            workout_session=workout_session,
            exercise=session_exercise_data["exercise"],
            notes=session_exercise_data.get("notes", ""),
        )

        for set_data in session_exercise_data.get("sets", []):
            WorkoutSessionExerciseSet.objects.create(
                session_exercise=session_exercise,
                reps=set_data["reps"],
                weight=set_data["weight"],
            )
    workout_session.save()
    return workout_session
