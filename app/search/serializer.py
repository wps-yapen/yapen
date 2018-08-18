# 버튼 검색 결과로 보여줄 room의 filed만 가진 serailizer(기존 base+ pension, pension의 사진, 이름,pk)
from location.serializer.pension import PensionNameSerializer, PensionImageSerializer
from location.serializer.room import RoomBaseSerializer


# 버튼 검색 결과로 보여줄 room의 field로 들어갈 pensio객체 serialize 하기위한 것
class PensionButtonSerachResultSerializer(PensionNameSerializer):
    rooms = RoomBaseSerializer(many=True, read_only=True)
    pensionimages = PensionImageSerializer(many=True, read_only=True)

    class Meta(PensionNameSerializer.Meta):
        fields = PensionNameSerializer.Meta.fields + (
            'pensionimages',
            'rooms',
        )



######@@@@@@@@@@@@@@@@@ 이하 임시저장. 참고만 해라. 나중에 지우도록 해라.
class RoomButtonSearchResultSerializer(RoomBaseSerializer):
    pension = PensionButtonSerachResultSerializer(read_only=True)

    class Meta(RoomBaseSerializer.Meta):
        fields = RoomBaseSerializer.Meta.fields +(
            'pension',
        )



