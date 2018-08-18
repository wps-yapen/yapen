import datetime

from django.db.models import Q
from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView

from location.models import Pension, Room
from location.serializer.pension import PensionListSerializer
import django_filters

from location.serializer.room import RoomBaseSerializer
from reservation.models import Reservation
from search.serializer import RoomButtonSearchResultSerializer, PensionButtonSerachResultSerializer



def convert_to_datetime(date):
    list1 = date.split('-')
    year = int(list1[0])
    month = int(list1[1])
    day = int(list1[2])
    target_date = datetime.date(year, month, day)
    return target_date



class KeyWordSearch(generics.ListCreateAPIView):
    serializer_class = PensionListSerializer

    # filter_backends 의 경우 반드시 튜플로 쉼표를 적어야 한다.
    filter_backends = (filters.SearchFilter,)
    queryset = Pension.objects.all()
    search_fields = ('name','theme',)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@       임시 저장함.

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
    serializer_class = RoomButtonSearchResultSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = ButtonFilter

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    임시저장함.





class ButtonPensionSearch(APIView):

    def get(self,request,format=None):
        get_data = request.query_params

        # url prarm에 넣은 것들만 Q로된 list에 추가해서 fitler할때 활용하겠다. (이렇게 안하면 애러뜸.)
        q_filter_objects = Q()
        q_exclude_objects = Q()

        if get_data.get('sub_location_no')!=None:
            q_filter_objects.add(Q(sub_location__sub_location_no=get_data.get('sub_location_no')),Q.AND)
        if get_data.get('max_num_people')!=None:
            q_filter_objects.add(Q(rooms__max_num_people__gte=get_data.get('max_num_people')),Q.AND)

        # theme의 경우는 url에서 , 으로 구분해서 받아서 여기서 for문 돌면서 Q로된 list에 추가해준다.
        if get_data.get('theme')!=None:
            # 일단 ',' 기준으로 분리해서 리스트를 만들고
            theme_list = get_data.get('theme').split(',')
            for theme in theme_list:
                q_filter_objects.add(Q(theme__contains=theme), Q.AND)

        # 가격
        if get_data.get('from_price')!=None and get_data.get('to_price')!=None:
            q_filter_objects.add(Q(rooms__price__gte=get_data.get('from_price')),Q.AND)
            q_filter_objects.add(Q(rooms__price__lte=get_data.get('to_price')),Q.AND)

        # 예약 겹치는 방 가진 pension 제외하는 Q
        if get_data.get('checkin_date')!=None and get_data.get('stay_day_num')!=None:
            checkin_date = convert_to_datetime(get_data.get('checkin_date'))
            stay_day_num = get_data.get('stay_day_num')
            checkout_date = checkin_date + \
                            datetime.timedelta(int(stay_day_num) - 1)

            # 주어진 date와 걸치는 reservation들 전체 reservation 들에서 뽑아봄.
            reservations_list_crush_with_given_date= Reservation.objects.filter(
                Q(checkout_date__gte=checkin_date,checkin_date__lte=checkin_date) |
                Q(checkin_date__lte=checkout_date, checkin_date__gte=checkin_date),).distinct()

            # 그런 reservation 가지고 있지 않은 방들의 pk만 뽑아봄.
            rooms = Room.objects.exclude(reservations__in=reservations_list_crush_with_given_date)

            # 그런 방들의 pk를 하나라도 가지고 있는 pension 을 뽑음.
            q_filter_objects.add(Q(rooms__in=rooms), Q.AND)

        pensions = Pension.objects.filter(q_filter_objects).distinct()

        serializer = PensionButtonSerachResultSerializer(pensions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)











