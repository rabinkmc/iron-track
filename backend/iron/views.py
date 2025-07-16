from rest_framework.response import Response
from rest_framework.views import APIView

from iron.models import Exercise
from iron.serializers import ExerciseSerializer, WorkoutSessionSerializer


class ExerciseView(APIView):
    def get(self, _):
        exercises = ExerciseSerializer(Exercise.objects.all(), many=True)
        return Response(exercises.data)

    def post(self, request):
        data = ExerciseSerializer(data=request.data)
        if not data.is_valid():
            return Response(data.errors, status=400)
        data.save()
        return Response(data.data, status=201)

    def put(self, request):
        exercise = Exercise.objects.filter(id=request.data["id"]).first()
        ser = ExerciseSerializer(exercise, data=request.data)
        if not exercise:
            return Response({"error": "Exercise not found"}, status=404)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        ser.save()
        return Response(ser.data, status=200)

    def delete(self, request, pk):
        try:
            exercise = Exercise.objects.get(pk=pk)
            exercise.delete()
            return Response(status=204)
        except Exercise.DoesNotExist:
            return Response({"error": "Exercise not found"}, status=404)


class WorkoutSessionView(APIView):
    def get(self, request):
        user = request.user
        workout_sessions = user.workout_sessions.select_related("exercises").all()
        ser = WorkoutSessionSerializer(workout_sessions, many=True)
        return Response(ser.data)

    def post(self, request):
        ser = WorkoutSessionSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        ser.save()
        return Response(ser.data, status=201)
