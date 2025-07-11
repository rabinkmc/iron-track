from rest_framework import serializers
from .models import Lift


class LiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lift
        fields = ["id", "user", type", "reps", "sets", "weights"]
