from django.shortcuts import get_object_or_404
from datetime import date

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status

from iron.models import (
    Exercise,
    WorkoutSessionExercise,
    WorkoutSessionExerciseSet,
)
from iron.serializers import (
    ExerciseCreateSerializer,
    ExerciseSerializer,
    WorkoutSessionCreateSerializer,
    WorkoutSessionExerciseSerializer,
    WorkoutSessionExerciseSetSerializer,
    WorkoutSessionSerializer,
)

from iron.services import update_exercise


class ExerciseViewSet(ViewSet):
    def list(self, _):
        ser = ExerciseSerializer(Exercise.objects.all(), many=True)
        return Response(ser.data)

    def retrieve(self, request, pk):
        exercise = get_object_or_404(Exercise, pk=pk)
        exercises = ExerciseSerializer(exercise)
        return Response(exercises.data)

    def create(self, request):
        ser = ExerciseCreateSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        Exercise.objects.create(**ser.data)
        return Response(status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        exercise = Exercise.objects.filter(pk=pk).first()
        if not exercise:
            return Response({"error": "Exercise not found"}, status=404)
        ser = ExerciseCreateSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        update_exercise(exercise, ser.data)
        return Response(status=200)

    def destroy(self, request, pk):
        exercise = get_object_or_404(Exercise, pk=pk)
        exercise.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WorkoutSessionViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        workout_sessions = user.workout_sessions.prefetch_related(
            "session_exercises", "session_exercises__sets"
        ).all()
        ser = WorkoutSessionSerializer(workout_sessions, many=True)
        return Response(ser.data)

    def retrieve(self, request, pk):
        workout_session = request.user.workout_sessions.filter(pk=pk).first()
        if not workout_session:
            return Response(
                {"error": "Workout session not found"}, status=status.HTTP_404_NOT_FOUND
            )
        ser = WorkoutSessionSerializer(workout_session)
        return Response(ser.data)

    def create(self, request):
        ser = WorkoutSessionCreateSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        today = date.today()
        user = request.user
        workout_session = user.workout_sessions.create(
            date=today, notes=ser.data.get("notes", "")
        )
        data = WorkoutSessionSerializer(workout_session).data
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        workout_session = request.user.workout_sessions.filter(pk=pk).first()
        if not workout_session:
            return Response({"error": "Workout session not found"}, status=404)
        ser = WorkoutSessionSerializer(workout_session, data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        workout_session.notes = ser.data.get("notes", "")
        workout_session.save()
        return Response(ser.data)


class WorkoutSessionExercisesViewSet(ViewSet):
    def create(self, request, pk):
        workout_session = request.user.workout_sessions.filter(pk=pk).first()
        if not workout_session:
            return Response(
                {"error": "Workout session not found"}, status=status.HTTP_404_NOT_FOUND
            )
        ser = WorkoutSessionExerciseSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        exercise = ser.validated_data["exercise"]
        WorkoutSessionExercise.objects.create(
            workout_session=workout_session,
            exercise=exercise,
            notes=ser.validated_data.get("notes", ""),
        )
        return Response(status=status.HTTP_201_CREATED)

    def list(self, request, pk):
        excercise = WorkoutSessionExercise.objects.all()
        if not excercise:
            return Response(
                {"error": "Workout session not found"}, status=status.HTTP_404_NOT_FOUND
            )
        ser = WorkoutSessionExerciseSerializer(excercise, many=True)
        return Response(ser.data)


class WorkoutSessionExerciseSetViewSet(ViewSet):
    """
    we will receive session exercise id

    1. ability to add sets to a session exercise
    2. ability to list sets of a session exercise
    """

    def create(self, request, pk):
        session_exercise = WorkoutSessionExercise.objects.filter(pk=pk).first()
        if not session_exercise:
            return Response(
                {"error": "Workout session exercise not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        ser = WorkoutSessionExerciseSetSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        WorkoutSessionExerciseSet(
            session_exercise=session_exercise,
            reps=ser.validated_data["reps"],
            weight=ser.validated_data["weight"],
        )
        return Response(status=status.HTTP_201_CREATED)

    def list(self, request, pk):
        session_exercise = WorkoutSessionExercise.objects.filter(pk=pk).first()
        if not session_exercise:
            return Response(
                {"error": "Workout session exercise not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        sets = session_exercise.sets.all()  # type: ignore
        ser = WorkoutSessionExerciseSetSerializer(sets, many=True)
        return Response(ser.data)
