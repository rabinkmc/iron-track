from django.db import models
from common.models import BaseModel


class Lifts(BaseModel):
    type = models.CharField(max_length=10)
    reps = models.PositiveSmallIntegerField()
    sets = models.PositiveSmallIntegerField()
