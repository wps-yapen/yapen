from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer.location import LocationSerializer, SubLocationSerializer
from .serializer.pension import PensionDetailSerializer, PensionListSerializer
from .models import Pension, Location, SubLocation


class PensionLocationsList(APIView):

    def get(self,request,format=None):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)

        # new_serializer_data = list(serializer.data)
        # new_serializer_data.append({'dict_key': 'dict_value'})
        # return Response(new_serializer_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PensionSubLocationList(APIView):

    def get_object(self, sub_location_no):
        try:
            return  SubLocation.objects.get(sub_location_no=sub_location_no)
        except SubLocation.DoesNotExist:
            raise Http404

    def get(self,request,sub_location_no,format=None):
        sublocation = self.get_object(sub_location_no=sub_location_no)
        serializer = SubLocationSerializer(sublocation)
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

