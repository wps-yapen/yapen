from django.http import Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import PensionDetailSerializer, PensionListSerializer
from .models import Pension


class PensionList(APIView):

    def get(self,request,format=None):
        pension = Pension.objects.all()
        serializer = PensionListSerializer(pension, many=True)
        return Response(serializer.data)


class PensionDetail(APIView):

    def get_object(self, pk):
        try:
            return Pension.objects.get(pk=pk)
        except Pension.DoesNotExist:
            raise Http404

    def get(self,request,pk,format=None):
        pension = self.get_object(pk=pk)
        serializer = PensionDetailSerializer(pension)
        return Response(serializer.data)