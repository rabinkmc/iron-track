from rest_framework.response import Response
from rest_framework.views import APIView

from iron.models import Exercise
from iron.serializers import ExerciseSerializer


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
        data = ExerciseSerializer(exercise, data=request.data, partial=True)
        if not data.is_valid():
            return Response(data.errors, status=400)
        if not exercise:
            return Response({"error": "Exercise not found"}, status=404)
        data.save()

    def delete(self, request, pk):
        try:
            exercise = Exercise.objects.get(pk=pk)
            exercise.delete()
            return Response(status=204)
        except Exercise.DoesNotExist:
            return Response({"error": "Exercise not found"}, status=404)
