from django.shortcuts import get_object_or_404
from datetime import date

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.generics import get_object_or_404

from iron.models import (
    Exercise,
    WorkoutSessionExercise,
    WorkoutSessionExerciseSet,
)
from iron.serializers import (
    ExerciseCreateSerializer,
    ExerciseSerializer,
    WorkoutSessionCreateSerializer,
    WorkoutSessionExerciseCreateSerializer,
    WorkoutSessionExerciseSerializer,
    WorkoutSessionExerciseSetCreateSerializer,
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
        exercise = get_object_or_404(Exercise, pk=pk)
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
        workout_session = get_object_or_404(request.user.workout_sessions, pk=pk)
        ser = WorkoutSessionSerializer(workout_session)
        return Response(ser.data)

    def create(self, request):
        ser = WorkoutSessionCreateSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        workout_date = ser.validated_data.get("date") or date.today()
        user = request.user
        workout_session = user.workout_sessions.create(
            date=workout_date, notes=ser.data.get("notes", "")
        )
        data = WorkoutSessionSerializer(workout_session).data
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        workout_session = get_object_or_404(request.user.workout_sessions, pk=pk)
        ser = WorkoutSessionCreateSerializer(workout_session, data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        workout_session.notes = ser.validated_data.get("notes", "")
        if ser.data.get("date"):
            workout_session.date = ser.validated_data["date"]
        workout_session.save()
        return Response(ser.data)


class WorkoutSessionExercisesViewSet(ViewSet):
    def create(self, request):
        workout_session = get_object_or_404(
            request.user.workout_sessions, pk=request.data.get("workout_session")
        )
        ser = WorkoutSessionExerciseCreateSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        exercise = ser.validated_data["exercise"]
        WorkoutSessionExercise.objects.create(
            workout_session=workout_session,
            exercise=exercise,
            notes=ser.validated_data.get("notes", ""),
        )
        return Response(status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        session_exercise = get_object_or_404(WorkoutSessionExercise, pk=pk)
        ser = WorkoutSessionExerciseCreateSerializer(
            session_exercise, data=request.data
        )
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        session_exercise.exercise = ser.validated_data["exercise"]
        session_exercise.notes = ser.validated_data.get("notes", "")
        session_exercise.save()
        return Response(status=status.HTTP_200_OK)

    def list(self, request):
        excercise = WorkoutSessionExercise.objects.all()
        ser = WorkoutSessionExerciseSerializer(excercise, many=True)
        return Response(ser.data)


class WorkoutSessionExerciseSetViewSet(ViewSet):
    """
    we will receive session exercise id

    1. ability to add sets to a session exercise
    2. ability to list sets of a session exercise
    """

    def create(self, request):
        session_exercise = get_object_or_404(
            WorkoutSessionExercise, pk=request.data.get("session_exercise")
        )
        ser = WorkoutSessionExerciseSetCreateSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        WorkoutSessionExerciseSet.objects.create(
            session_exercise=session_exercise,
            reps=ser.validated_data["reps"],
            weight=ser.validated_data["weight"],
        )
        return Response(status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        session_exercise_set = get_object_or_404(WorkoutSessionExerciseSet, pk=pk)
        ser = WorkoutSessionExerciseSetCreateSerializer(
            session_exercise_set, data=request.data
        )
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        session_exercise_set.reps = ser.validated_data["reps"]
        session_exercise_set.weight = ser.validated_data["weight"]
        session_exercise_set.save()
        return Response(status=status.HTTP_200_OK)

    def list(self, request):
        """
        list all exercise sets for the authenticated user
        """
        sets = WorkoutSessionExerciseSet.objects.filter(
            session_exercise__workout_session__user=request.user
        ).select_related("session_exercise__exercise")
        ser = WorkoutSessionExerciseSetSerializer(sets, many=True)
        return Response(ser.data)
