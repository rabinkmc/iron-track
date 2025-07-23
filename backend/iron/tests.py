from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from iron.models import Exercise, WorkoutSession, WorkoutSessionExercise
from iron.serializers import WorkoutSessionExerciseSetCreateSerializer

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
