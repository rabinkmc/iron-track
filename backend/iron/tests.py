from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from iron.models import (
    Exercise,
    WorkoutSession,
    WorkoutSessionExercise,
    WorkoutSessionExerciseSet,
)

User = get_user_model()


class SessionCreateTest(APITestCase):
    def setUp(self):
        """
        create a user and force login
        """
        self.user = User.objects.create_user(username="admin", password="admin")  # type: ignore
        self.client.force_login(self.user)

    def test_session_create(self):
        """
        Test creating a workout session
        """
        url = reverse("iron:session-list")
        response = self.client.post(
            url,
            data={
                "date": "2023-10-01",
                "notes": "Felt great!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            WorkoutSession.objects.filter(user=self.user, date="2023-10-01").exists()
        )

    def test_workout_session_update(self):
        workout = WorkoutSession.objects.create(
            user=self.user, date="2023-10-01", notes="Initial notes"
        )
        url = reverse("iron:session-detail", kwargs={"pk": workout.pk})
        response = self.client.put(
            url,
            data={
                "date": "2023-10-02",
                "notes": "Updated notes",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        workout.refresh_from_db()
        self.assertTrue(
            WorkoutSession.objects.filter(
                user=self.user, date="2023-10-02", notes="Updated notes"
            ).exists()
        )


class ExerciseCreateTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="admin")  # type: ignore
        self.client.force_login(self.user)

    def test_exercise_create(self):
        """
        Test creating an exercise
        """
        url = reverse("iron:exercise-list")
        response = self.client.post(
            url,
            data={
                "name": "Bench Press",
                "muscle_targeted": "Chest",
                "description": "A compound exercise for the chest.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Exercise.objects.filter(
                name="Bench Press",
                muscle_targeted="Chest",
                description="A compound exercise for the chest.",
            ).exists()
        )

    def test_exercise_update(self):
        exercise = Exercise.objects.create(
            name="Bench Press",
            muscle_targeted="Chest",
            description="A compound exercise for the chest.",
        )
        url = reverse("iron:exercise-detail", kwargs={"pk": exercise.pk})
        response = self.client.put(
            url,
            data={
                "name": "Bench Press Updated",
                "muscle_targeted": "Chest",
                "description": "Updated description.",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        exercise.refresh_from_db()
        self.assertEqual(exercise.name, "Bench Press Updated")
        self.assertEqual(exercise.description, "Updated description.")


class WorkoutSessionExerciseTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="admin", password="admin")  # type: ignore
        self.client.force_login(self.user)

    def test_workout_session_exercise_create(self):
        """
        Test creating a workout session exercise
        """
        session = WorkoutSession.objects.create(user=self.user, date="2023-10-01")
        exercise = Exercise.objects.create(
            name="Squat",
            muscle_targeted="Legs",
            description="A compound exercise for the legs.",
        )

        url = reverse("iron:session-exercise-list")
        response = self.client.post(
            url,
            data={
                "workout_session": session.pk,
                "exercise": exercise.pk,
                "notes": "Felt strong today!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            WorkoutSessionExercise.objects.filter(
                workout_session=session, exercise=exercise
            ).exists()
        )

    def test_workout_session_exercise_update(self):
        session = WorkoutSession.objects.create(user=self.user, date="2023-10-01")
        exercise = Exercise.objects.create(
            name="Squat",
            muscle_targeted="Legs",
            description="A compound exercise for the legs.",
        )
        session_exercise = WorkoutSessionExercise.objects.create(
            workout_session=session, exercise=exercise, notes="Initial notes"
        )

        url = reverse(
            "iron:session-exercise-detail", kwargs={"pk": session_exercise.pk}
        )
        response = self.client.put(
            url,
            data={
                "workout_session": session.pk,
                "notes": "Updated notes",
                "exercise": exercise.pk,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        session_exercise.refresh_from_db()
        self.assertEqual(session_exercise.notes, "Updated notes")


class WorkoutSessionExcerciseSetTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="admin", password="admin")  # type: ignore
        self.client.force_login(self.user)

    def test_workout_session_exercise_set_create(self):
        """
        Test creating a workout session exercise set
        """
        session = WorkoutSession.objects.create(user=self.user, date="2023-10-01")
        exercise = Exercise.objects.create(
            name="Deadlift",
            muscle_targeted="Back",
            description="A compound exercise for the back.",
        )
        session_exercise = WorkoutSessionExercise.objects.create(
            workout_session=session, exercise=exercise
        )

        url = reverse("iron:exercise-set-list")
        response = self.client.post(
            url,
            data={
                "session_exercise": session_exercise.pk,
                "reps": 10,
                "weight": 100.0,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            WorkoutSessionExerciseSet.objects.filter(
                session_exercise=session_exercise, reps=10, weight=100.0
            ).exists()
        )

    def test_workout_session_exercise_set_update(self):
        session = WorkoutSession.objects.create(user=self.user, date="2023-10-01")
        exercise = Exercise.objects.create(
            name="Deadlift",
            muscle_targeted="Back",
            description="A compound exercise for the back.",
        )
        session_exercise = WorkoutSessionExercise.objects.create(
            workout_session=session, exercise=exercise
        )
        session_exercise_set = WorkoutSessionExerciseSet.objects.create(
            session_exercise=session_exercise, reps=10, weight=100.0
        )

        url = reverse(
            "iron:exercise-set-detail", kwargs={"pk": session_exercise_set.pk}
        )
        response = self.client.put(
            url,
            data={
                "session_exercise": session_exercise.pk,
                "reps": 12,
                "weight": 110.0,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        session_exercise_set.refresh_from_db()
        self.assertEqual(session_exercise_set.reps, 12)
        self.assertEqual(session_exercise_set.weight, 110.0)

    def test_workout_session_bulk_create(self):
        url = reverse("iron:session-bulk-create")
        ex1 = Exercise.objects.create(
            name="Barbell Squat",
            muscle_targeted="Legs",
            description="A compound exercise for the legs.",
        )
        ex2 = Exercise.objects.create(
            name="Leg Press",
            muscle_targeted="Legs",
            description="A compound exercise for the legs.",
        )
        response = self.client.post(
            url,
            data={
                "user": self.user.pk,
                "date": "2025-07-22",
                "notes": "I did 3 exercises for legs; barbell squat, leg press, standing calf raises.",
                "session_exercises": [
                    {
                        "exercise": ex1.pk,
                        "notes": "I maxed out today, was feeling good.",
                        "sets": [
                            {"reps": 5, "weight": "60.00"},
                            {"reps": 5, "weight": "80.00"},
                        ],
                    },
                    {
                        "exercise": ex2.pk,
                        "notes": "",
                        "sets": [
                            {"reps": 10, "weight": "70.00"},
                            {"reps": 12, "weight": "120.00"},
                        ],
                    },
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            WorkoutSession.objects.filter(user=self.user, date="2025-07-22").exists()
        )
        self.assertTrue(WorkoutSessionExercise.objects.count() == 2)

        self.assertTrue(WorkoutSessionExerciseSet.objects.count() == 4)

    def test_session_list(self):
        workout_session = WorkoutSession.objects.create(
            user=self.user, date="2023-10-01", notes="Test session"
        )
        leg_press = Exercise.objects.create(
            name="Leg Press",
            muscle_targeted="Legs",
            description="A compound exercise for the legs.",
        )
        barbell_squat = Exercise.objects.create(
            name="Barbell Squat",
            muscle_targeted="Legs",
            description="A compound exercise for the legs.",
        )
        leg_press_session = WorkoutSessionExercise.objects.create(
            workout_session=workout_session,
            exercise=leg_press,
            notes="Leg press notes",
        )
        barbell_squat_session = WorkoutSessionExercise.objects.create(
            workout_session=workout_session,
            exercise=barbell_squat,
            notes="Barbell squat notes",
        )
        WorkoutSessionExerciseSet.objects.create(
            session_exercise=leg_press_session, reps=10, weight=100.0
        )
        WorkoutSessionExerciseSet.objects.create(
            session_exercise=leg_press_session, reps=8, weight=120.0
        )
        WorkoutSessionExerciseSet.objects.create(
            session_exercise=barbell_squat_session, reps=5, weight=150.0
        )
        WorkoutSessionExerciseSet.objects.create(
            session_exercise=barbell_squat_session, reps=6, weight=160.0
        )
        url = reverse("iron:session-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)

        url = reverse("iron:session-detail", kwargs={"pk": workout_session.pk})
        print(response.json())
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
