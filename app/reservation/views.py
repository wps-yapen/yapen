import datetime
import re

from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from location.models import Room
from location.serializer import pension
from reservation.models import Reservation
from reservation.serializer.reservation import RoomReservationSerializer


class ReservationRoom(APIView):
	def get(self, request, pk, date, format=None):
		list1 = date.split('-')
		year = int(list1[0])
		month = int(list1[1])
		day = int(list1[2])
		target_date = datetime.date(year, month, day)
		reservated_list = Reservation.objects.filter(checkin_date__lte = target_date, checkout_date__gte = target_date)
		reservated_room_pk_list = []
		for reservation in reservated_list:
			if reservation.room.pension.pk == pk:
				reservated_room_pk_list.append(reservation.room.pk)
		rooms = Room.objects.filter(pension=pk).exclude(pk__in=reservated_room_pk_list)
		serializer = RoomReservationSerializer(rooms, many=True)
		return Response(serializer.data)
