from django.contrib.auth import get_user_model
from django.db import models
from common.models import BaseModel

User = get_user_model()


class Lift(BaseModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="lifts")
    type = models.CharField(max_length=10)
    reps = models.PositiveSmallIntegerField()
    sets = models.PositiveSmallIntegerField()
    weights = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.type} {self.weights} kg ({self.reps} * {self.sets})"
