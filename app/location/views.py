from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer.room import RoomReservationSerializer, RoomSerializer
from .serializer.pension import PensionDetailSerializer, PensionListSerializer
from .models import Pension, Room


class PensionList(APIView):

    def get(self,request,format=None):
        pensions = Pension.objects.all()
        serializer = PensionListSerializer(pensions, many=True)

        # new_serializer_data = list(serializer.data)
        # new_serializer_data.append({'dict_key': 'dict_value'})
        # return Response(new_serializer_data)
        return Response(serializer.data)


class PensionLocationList(APIView):

    def get(self,request,sub_location_no,format=None):
        pensions = Pension.objects.filter(Q(sub_location_no=sub_location_no))
        serializer = PensionListSerializer(pensions,many=True)
        return Response(serializer.data)


class PensionDetail(APIView):

    def get_object(self, pk):
        try:
            return Pension.objects.get(pk=pk)
        except Pension.DoesNotExist:
            raise Http404

    def get(self,request,sub_location_no,pk,format=None):
        pension = self.get_object(pk=pk)
        serializer = PensionDetailSerializer(pension)
        return Response(serializer.data)


class ReservationRoomList(APIView):

    def get(self,request,pk,format=None):
        pension=Pension.objects.get(pk=pk)
        rooms = Room.objects.filter(Q(pension=pension))
        serializer = RoomReservationSerializer(rooms, many=True)
        return Response(serializer.data)