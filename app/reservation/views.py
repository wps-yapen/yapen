import datetime
import re

import django
from django.db.models import Q
from django.http import Http404, HttpResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from location.models import Room
from location.serializer import pension
from location.serializer.room import RoomBaseSerializer
from reservation.models import Reservation
from reservation.serializer.payment import ReservationPaySerializer
from reservation.serializer.reservation import RoomReservationSerializer
import json



def convert_to_datetime(date):
    list1 = date.split('-')
    year = int(list1[0])
    month = int(list1[1])
    day = int(list1[2])
    target_date = datetime.date(year, month, day)
    return target_date


    # 요청에 넣을것. x
    # http://localhost:8000/reservation/2/2018-08-08/ 주소에  팬션pk, date 받아서 씀

class ReservationRoom(APIView):

    def get(self, request, pk, date, format=None):
        list1 = date.split('-')
        year = int(list1[0])
        month = int(list)

    def get(self,request,pk, date, format=None):
        target_date = convert_to_datetime(date)
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
        return Response(serializer.data,status=status.HTTP_200_OK)

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
        room = self.get_room_object(pk=rooom_pk)


        # 묵으려는 박수가 다른 reservatino 과 겹치면?
        # 즉 checkoutdate가 다른 reservation 의 날짜 range안에 들어있다면?
        checkin_date = convert_to_datetime(request.data.get('checkin_date'))
        checkout_date =  checkin_date + \
                      datetime.timedelta(int(request.data.get('stay_day_num'))- 1)
        reservation = room.reservations.filter(Q(checkout_date__lte=checkout_date, checkout_date__gte=checkin_date)|
        Q(checkin_date__lte=checkout_date, checkin_date__gte=checkin_date))

        # 만약 그런 reservatoin이 있다면 에러를 400에러를 raise한다.
        if reservation:
            return Response(status=status.HTTP_400_BAD_REQUEST)


        # room 관련 정보는 roombaseserializer로 뽑아오겠슴.
        serializer = RoomBaseSerializer(room)

        # 최종적으로 전달할 정보들 담은 dit
        new_serializer_data = dict(serializer.data)

        # 여기에 request로 받은 정보들을 update
        new_serializer_data.update(request.data)

        return Response(new_serializer_data,status=status.HTTP_200_OK)


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

        #
        # # 해당되는 방에 있는 Reservation 객체들언 먼저 다 가져온다.
        # reservations_of_this_room = Reservation.objects.filter(room=request.data.get("pk"),
        #                                                        checkin_date__lte=target_date,
        #                                                        checkout_date__gte=target_date)




    # 요청에 넣을것.----------->Reservation 객체 만들때 필요한 모든것.

    # {
    #     "pk": "1",
    #     "checkin_date": "2018-08-13",
    #     "stay_day_num": "4",
    #     "total_price": "4000000",
    #     "subscriber": "maro's_friends",
    #     "phone_number": "010-6651-1550",
    #     "method_of_payment": "무통장입금",
    #     "deposit_bank": "우리은행",
    #     "depositor_name": "나산마로",
    #     "card_number": "5342-9200-0247-2223",
    #
    #     "expiration_month": "01",
    #     "expiration_year": "30",
    #     "card_password": "29",
    #     "card_type": "개인",
    #     "birth_date_of_owner": "19920803",
    #     "installment_plan": "2개월",
    #     "email": "nadcdc4@gmail.com"
    # }


class ReservationPay(APIView):

    # room 객체 얻는 함수 없으면 404에러
    def get_room_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise Http404


    def post(self,request, format=None):

        # 로그인이 안되있으면 (받은 요청의 헤더에 토큰이 없으면) 에러 발생
        if type(request.user) == django.contrib.auth.models.AnonymousUser:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


        reservation = Reservation.objects.create(
            room=self.get_room_object(pk=request.data.get('pk')),
            user=request.user,
            checkin_date=convert_to_datetime(request.data.get('checkin_date')),
            checkout_date=convert_to_datetime(request.data.get('checkin_date')) +
                          datetime.timedelta(int(request.data.get('stay_day_num'))- 1),
            total_price=int(request.data.get("total_price")),
            subscriber=request.data.get("subscriber"),
            phone_number=request.data.get("phone_number"),
            method_of_payment=request.data.get("method_of_payment"),
        )
        # 지불 방법에 따라 다르게 업데이트해야한다.
        if request.data.get("method_of_payment") == "무통장입금":
            reservation.deposit_bank = request.data.get("deposit_bank")
            reservation.depositor_name = request.data.get("depositor_name")

        elif request.data.get("method_of_payment") == "카드간편결제":
            reservation.card_number = request.data.get("card_number")
            reservation.expiration_month = request.data.get("expiration_month")
            reservation.expiration_year = request.data.get("expiration_year")
            reservation.card_password = request.data.get("card_password")
            reservation.card_type = request.data.get("card_type")
            reservation.birth_date_of_owner = request.data.get("birth_date_of_owner")
            reservation.installment_plan = request.data.get("installment_plan")
            reservation.email = request.data.get("email")
        reservation.save()

        return Response(request.data,status=status.HTTP_200_OK)


