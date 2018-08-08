from rest_framework.response import Response
from rest_framework.views import APIView

from location.models import Room
from location.serializer import pension
from reservation.serializer.reservation import RoomReservationSerializer


class ReservationRoom(APIView):
	def get(self, request, pk, format=None):
		rooms = Room.objects.filter(pension = pk, )
		serializer = RoomReservationSerializer(rooms, many=True)
		return Response(serializer.data)