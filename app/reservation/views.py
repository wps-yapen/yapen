import datetime
import re

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from location.models import Room
from location.serializer import pension
from reservation.models import Reservation
from reservation.serializer.payment import ReservationPaySerializer
from reservation.serializer.reservation import RoomReservationSerializer
import json

class ReservationRoom(APIView):

    def get(self, request, pk, date, format=None):
        list1 = date.split('-')
        year = int(list1[0])
        month = int(list)

    def get(self,request,pk, date, format=None):
        list1 = date.split('-')
        year = int(list1[0])
        month = int(list1[1])
        day = int(list1[2])
        target_date = datetime.date(year, month, day)
        reservated_list = Reservation.objects.filter(checkin_date__lte=target_date, checkout_date__gte=target_date)
        reservated_room_pk_list = []
        for reservation in reservated_list:
            if reservation.room.pension.pk == pk:
                reservated_room_pk_list.append(reservation.room.pk)
        rooms = Room.objects.filter(pension=pk).exclude(pk__in=reservated_room_pk_list)
        room_all =Room.objects.filter(pension=pk)

        for room in room_all:
            room.status = False
            room.save()

        for room in rooms:
            room.status = True
            room.save()

        rooms_all = Room.objects.filter(pension=pk)
        serializer = RoomReservationSerializer(rooms_all, many=True)
        return Response(serializer.data)


class ReservationPay(APIView):
    def post(self, request, pk, date, format=None):
        print(request.data)

        # serializer = json.parse(request.data)

        # 객실명,           ----->room.pk로부터 받아서 넣자.
        # 기준/최대인원,------>room.pk로부터 받아서 넣자.
        # 이용일,         -----> 예약페이지에서 받아야함.
        # 인원,           ----->예약페이지에서 받아야함.
        # 결제금액,        ----->예약페이지에서 받아야함.



        return Response(request.data)


        # serializer = ReservationPaySerializer(data=request.data)
        #
        # if serializer.is_valid():
        #     print('imhere@@@@@@@@@@@@@@@@@@@@@@@@@@@2')
        #     serializer.save()
        #
        #     return Response(serializer.validated_data, status=status.HTTP_200_OK)
        # return Response(status=status.HTTP_400_BAD_REQUEST)
        #






