from rest_framework import generics,  filters

from location.models import  Pension
from location.serializer.pension import PensionListSerializer



class KeyWordButtonSearch(generics.ListCreateAPIView):
    serializer_class = PensionListSerializer

    # filter_backends 의 경우 반드시 튜플로 쉼표를 적어야 한다.
    filter_backends = (filters.SearchFilter,)
    queryset = Pension.objects.all()
    search_fields = ('name','theme',)