from rest_framework import generics,  filters
from location.models import Pension, Room
from location.serializer.pension import PensionListSerializer
import django_filters

from location.serializer.room import RoomBaseSerializer


class KeyWordSearch(generics.ListCreateAPIView):
    serializer_class = PensionListSerializer

    # filter_backends 의 경우 반드시 튜플로 쉼표를 적어야 한다.
    filter_backends = (filters.SearchFilter,)
    queryset = Pension.objects.all()
    search_fields = ('name','theme',)


class ButtonFilter(django_filters.rest_framework.FilterSet):
    sub_location_no = django_filters.CharFilter("pension__sub_location__sub_location_no")
    max_num_people = django_filters.NumberFilter("max_num_people", lookup_expr='lte')
    theme = django_filters.CharFilter("pension__theme",lookup_expr='contains')
    from_price = django_filters.NumberFilter("price", lookup_expr='gte')
    to_price = django_filters.NumberFilter("price", lookup_expr='lte')



    # pension__theme__contains

    class Meta:
        model = Room
        fields = [
            'sub_location_no',
            'max_num_people',
            'theme','from_price',
            'to_price',
        ]


class ButtonSearch(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomBaseSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = ButtonFilter