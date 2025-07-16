def update_exercise(exercise, data):
    exercise.name = data["name"]
    exercise.muscle_targeted = data["muscle_targeted"]
    exercise.description = data.get("description", "")
    exercise.save()
    return exercise
