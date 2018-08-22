from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer.location import LocationSerializer, SubLocationSerializer, IosLocationSerializer, \
    IosSubLocationSerializer
from .serializer.pension import PensionDetailSerializer, PensionListSerializer
from .models import Pension, Location, SubLocation, Room


# IOS 요청으로 예비로 만들어놈.
class IosPensionMainList(APIView):

    def get(self,request,format=None):
        locations = Location.objects.all()
        serializer = IosLocationSerializer(locations, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

# IOS 요청으로 예비로 만들어놈.
class IosPensionSubLocationList(APIView):

    def get(self,request,sub_location_no,format=None):
        sub_location = SubLocation.objects.filter(sub_location_no=sub_location_no)
        serializer = IosSubLocationSerializer(sub_location, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
