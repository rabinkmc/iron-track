from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from iron.models import WorkoutSession

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
