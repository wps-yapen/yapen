# 버튼 검색 결과로 보여줄 room의 filed만 가진 serailizer(기존 base+ pension, pension의 사진, 이름,pk)
import datetime

from django.db.models import Q

from location.models import Room
from location.serializer.pension import PensionNameSerializer, PensionImageSerializer
from location.serializer.room import RoomBaseSerializer
from rest_framework import serializers

from reservation.models import Reservation


def convert_to_datetime(date):
    list1 = date.split('-')
    year = int(list1[0])
    month = int(list1[1])
    day = int(list1[2])
    target_date = datetime.date(year, month, day)
    return target_date

# 버튼 검색 결과로 보여줄 room의 field로 들어갈 pensio객체 serialize 하기위한 것
class PensionButtonSerachResultSerializer(PensionNameSerializer):
    # rooms = RoomBaseSerializer(many=True, read_only=True)
    rooms = serializers.SerializerMethodField('get_result_rooms')

    def get_result_rooms(self, pension):

        # 팬션에 대한 filttering 할때 쓸 Q object
        q_filter_objects = Q()
        q_filter_objects.add(Q(pension=pension), Q.AND)

        # fillter 조건 값을 전달 받은 경우만 Q object에 추가한다.
        if self.context.get('max_num_people')!=None:
            q_filter_objects.add(Q(max_num_people__gte=self.context.get('max_num_people')),Q.AND)
        if self.context.get('from_price')!=None and self.context.get('to_price')!=None:
            q_filter_objects.add(Q(price__gte=self.context.get('from_price')),Q.AND)
            q_filter_objects.add(Q(price__lte=self.context.get('to_price')),Q.AND)
        if self.context.get('checkin_date')!=None and self.context .get('stay_day_num')!=None:
            checkin_date = convert_to_datetime(self.context.get('checkin_date'))
            stay_day_num = self.context.get('stay_day_num')
            checkout_date = checkin_date + \
                            datetime.timedelta(int(stay_day_num) - 1)

            # 주어진 date와 걸치는 reservation들 전체 reservation 들에서 뽑아봄.
            reservations_list_crush_with_given_date = Reservation.objects.filter(
                Q(checkout_date__gte=checkin_date, checkin_date__lte=checkin_date) |
                Q(checkin_date__lte=checkout_date, checkin_date__gte=checkin_date), ).distinct()

            # 그런 reservation 가지고 있지 않은 방들의 pk만 뽑아봄.
            rooms = Room.objects.exclude(reservations__in=reservations_list_crush_with_given_date)

            # 그런 방들의 pk 리스트 에 자신의 pk 가 포함되는 방을 뽑음.
            q_filter_objects.add(Q(pk__in=rooms), Q.AND)

        qs = Room.objects.filter(q_filter_objects).distinct()
        serializers = RoomButtonSearchResultSerializer(instance=qs,many=True)
        return serializers.data



    pensionimages = PensionImageSerializer(many=True, read_only=True)

    class Meta(PensionNameSerializer.Meta):
        fields = PensionNameSerializer.Meta.fields + (
            'pensionimages',
            'rooms',
        )

    # likes = serializers.SerializerMethodField('get_likes')
    #
    # def get_likes(self, product):
    #     qs = Like.objects.filter(whether_like=True, product=product)
    #     serializer = LikeSerializer(instance=qs, many=True)
    #     return serializer.data


######@@@@@@@@@@@@@@@@@ 이하 임시저장. 참고만 해라. 나중에 지우도록 해라.
class RoomButtonSearchResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = (
        'pk',
        'name',
        'size',
        'normal_num_poeple',
        'max_num_people',
        'price',
        )


