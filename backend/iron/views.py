from rest_framework.decorators import api_view
from rest_framework.response import Response

from iron.models import Lift
from iron.serializers import LiftSerializer


@api_view(["GET"])
def lift_list(request):
    curr_lift = Lift.objects.filter(user=request.user).first()
    curr_ser = LiftSerializer(curr_lift).data
    return Response(curr_ser)


@api_view(["POST"])
def create_lift(request):
    serializer = LiftSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
