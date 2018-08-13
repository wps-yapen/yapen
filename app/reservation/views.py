import datetime
import re

from django.db.models import Q
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from location.models import Room
from location.serializer import pension
from location.serializer.room import RoomBaseSerializer
from reservation.models import Reservation
from reservation.serializer.payment import ReservationPaySerializer
from reservation.serializer.reservation import RoomReservationSerializer
import json



    # 요청에 넣을것. x
    # http://localhost:8000/reservation/2/2018-08-08/ 주소에  팬션pk, date 받아서 씀

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

    # 결과
    # {
    #     "name": "스콜피오(전갈자리)",
    #     "size": "86㎡ (26평)",
    #     "normal_num_poeple": 4,
    #     "max_num_people": 8,
    #     "price": 200000,
    #     "pk": 1,
    #     "reservations": [],
    #     "extra_charge_adult": 20000,
    #     "extra_charge_child": 10000,
    #     "extra_charge_baby": 10000,
    #     "status": true
    # },







    # 요청에 넣을것.
    # {
    #     "pk": "1",                        pk를 요청에 넣는게 맞을지? 아니면 url에 ?------>방객체 자체를 pk로 특정화해놓고 고정적으로 쓰는게 아니라
    #     "checkin_date": "2018-08-13",                                               reservation/pk/info가 모든방에서 같으면 이상할듯.
    #     "stay_day_num": "4",                                                        그렇다고 쓰지도않는 datet를 url에 넣어도 이상할듯.
    #     "adult_num": "2",                                                           그렇다면 둘다 같이 넣어줄까 ?
    #     "child_num": "0",
    #     "baby_num": "0",
    #     "total_price": "4000000"
    # }

class ReservationInfo(APIView):

    # room 객체 얻는 함수 없으면 404에러
    def get_room_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise Http404



    def post(self, request, format=None):

        # 먼저 전달받은 pk로 해당 방 객체를 얻는다. 없으면 404 애러 띄움.
        rooom_pk = request.data.get('pk')

        # room 관련 정보는 roombaseserializer로 뽑아오겠슴.
        room = self.get_room_object(pk=rooom_pk)
        serializer = RoomBaseSerializer(room)

        # 최종적으로 전달할 정보들 담은 dit
        new_serializer_data = dict(serializer.data)

        # 여기에 request로 받은 정보들을 update
        new_serializer_data.update(request.data)

        return Response(new_serializer_data)


        # 결과

        # {
        #     "name": "스콜피오(전갈자리)",
        #     "size": "86㎡ (26평)",
        #     "normal_num_poeple": 4,
        #     "max_num_people": 8,
        #     "price": 200000,
        #     "pk": "1",
        #     "checkin_date": "2018-08-13",
        #     "stay_day_num": "4",
        #     "adult_num": "2",
        #     "child_num": "0",
        #     "baby_num": "0",
        #     "total_price": "4000000"
        # }










