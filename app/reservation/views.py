import datetime
import re

from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from location.models import Room
from location.serializer import pension
from reservation.serializer.reservation import RoomReservationSerializer


class ReservationRoom(APIView):
	def get(self, request, pk, date, format=None):
		list1 = date.split('-')
		year = int(list1[0])
		month = int(list1[1])
		day = int(list1[2])
		date_result = datetime.date(year, month, day)
		print(date_result)
		rooms = Room.objects.filter(reservations__checkin_date = date_result)
		serializer = RoomReservationSerializer(rooms, many=True)
		return Response(serializer.data)