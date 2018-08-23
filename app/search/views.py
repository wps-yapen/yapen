import datetime

from django.db.models import Q
from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView

from location.models import Pension, Room
from location.serializer.pension import PensionListSerializer
import django_filters

from reservation.models import Reservation
from search.serializer import RoomButtonSearchResultSerializer, PensionButtonSerachResultSerializer



def convert_to_datetime(date):
    list1 = date.split('-')
    year = int(list1[0])
    month = int(list1[1])
    day = int(list1[2])
    target_date = datetime.date(year, month, day)
    return target_date

# 가격을 숫자로 받은뒤 해당하는 range를 가져다 쓴다.
price_range_dict ={'0':(0,99999999),'1':(0,50000),'2':(50000,100000),'3':(100000,150000),'4':(150000,200000),'5':(200000,250000),
                   '6':(250000,300000),'7':(300000,350000),'8':(350000,400000),'9':(400000,9999999)}


class KeyWordSearch(generics.ListCreateAPIView):
    serializer_class = PensionListSerializer

    # filter_backends 의 경우 반드시 튜플로 쉼표를 적어야 한다.
    filter_backends = (filters.SearchFilter,)
    queryset = Pension.objects.all()
    search_fields = ('name','theme',)


class ButtonPensionSearch(APIView):

    def get(self,request,format=None):
        get_data = request.query_params

        # serializer에서 room field 를 filtering할때 쓸것 담을곳.
        context = dict()

        # url prarm에 넣은 것들만 Q로된 list에 추가해서 fitler할때 활용하겠다. (이렇게 안하면 애러뜸.)
        q_filter_objects = Q()

        if get_data.get('sub_location_no')!=None:
            q_filter_objects.add(Q(sub_location__sub_location_no=get_data.get('sub_location_no')),Q.AND)
        if get_data.get('max_num_people')!=None:
            q_filter_objects.add(Q(rooms__max_num_people__gte=get_data.get('max_num_people')),Q.AND)
            context['max_num_people'] = get_data.get('max_num_people')

        # theme의 경우는 url에서 , 으로 구분해서 받아서 여기서 for문 돌면서 Q로된 list에 추가해준다.
        if get_data.get('theme')!=None:
            # 일단 ',' 기준으로 분리해서 리스트를 만들고
            theme_list = get_data.get('theme').split(',')
            for theme in theme_list:
                q_filter_objects.add(Q(theme__contains=theme), Q.AND)

        # 가격
        if get_data.get('price_range')!=None:
            price_range = price_range_dict[get_data.get('price_range')]
            from_price = price_range[0]
            to_price = price_range[1]

            q_filter_objects.add(Q(rooms__price__gte=from_price),Q.AND)
            q_filter_objects.add(Q(rooms__price__lte=to_price),Q.AND)
            context['from_price'] = from_price
            context['to_price'] = to_price

        # if get_data.get('from_price') != None and get_data.get('to_price') != None:
            # q_filter_objects.add(Q(rooms__price__gte=get_data.get('from_price')),Q.AND)
            # q_filter_objects.add(Q(rooms__price__lte=get_data.get('to_price')),Q.AND)
            # context['from_price'] = get_data.get('from_price')
            # context['to_price'] = get_data.get('to_price')

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

            context['checkin_date'] = get_data.get('checkin_date')
            context['stay_day_num'] = get_data.get('stay_day_num')

        pensions = Pension.objects.filter(q_filter_objects).distinct()
        serializer = PensionButtonSerachResultSerializer(data=pensions, many=True,context=context)

        # 위에서 serializer 함수 호출시 data 표시해주면 is_valid에서 false이지만 어쨌든 Response에 넣어줄 수 있어서 이렇ㅔ했음.
        # pension을 그대로 위치인자로 주면 is_valid 자체를 검사조차 못한다.
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)










