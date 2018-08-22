from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializer.location import LocationSerializer, SubLocationSerializer
from ..serializer.pension import PensionDetailSerializer, PensionListSerializer
from ..models import Pension, Location, SubLocation, Room


# 검색창에서 쓰이는 Locaiton, SubLocation 의 name, location_no, pension수 보이기 위한 serailzie
class PensionLocationNamesList(APIView):

    def get(self,request,format=None):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)

        # new_serializer_data = list(serializer.data)
        # new_serializer_data.append({'dict_key': 'dict_value'})
        # return Response(new_serializer_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Main 페이지에서 모든 location에 속한 pension들을 보여주는 viwe
class PensionMainList(APIView):

    def get(self,request,format=None):
        pensions = Pension.objects.all()
        serializer = PensionListSerializer(pensions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# sub_location에 속한 pension들을 보여주는 view
class PensionSubLocationList(APIView):

    # def get_object(self, sub_location_no):
    #     try:
    #         sub_location = SubLocation.objects.get(sub_location_no=sub_location_no)
    #         return  Pension.objects.filter(sub_location=sub_location.pk)
    #     except SubLocation.DoesNotExist:
    #         raise Http404

    def get(self,request,sub_location_no,format=None):
        sub_location = SubLocation.objects.get(sub_location_no=sub_location_no)
        pensions = Pension.objects.filter(sub_location=sub_location.pk)
        serializer = PensionListSerializer(pensions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PensionDetail(APIView):

    def get_object(self, pk):
        try:
            return Pension.objects.get(pk=pk)
        except Pension.DoesNotExist:
            raise Http404

    def get(self,request,sub_location_no,pk,format=None):
        pension = self.get_object(pk=pk)
        serializer = PensionDetailSerializer(pension)
        return Response(serializer.data,status=status.HTTP_200_OK)

