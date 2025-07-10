from rest_framework.decorators import api_view
from rest_framework.response import Response

from iron.models import Lift
from iron.serializers import LiftSerializer


@api_view(["GET"])
def lift_list(request):
    curr_lift = Lift.objects.filter(user=request.user).first()
    curr_ser = LiftSerializer(curr_lift).data
    return Response(curr_ser)
