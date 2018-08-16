# 버튼 검색 결과로 보여줄 room의 filed만 가진 serailizer(기존 base+ pension, pension의 사진, 이름,pk)
from location.serializer.pension import PensionNameSerializer
from location.serializer.room import RoomBaseSerializer


# 버튼 검색 결과로 보여줄 room의 field로 들어갈 pensio객체 serialize 하기위한 것
class PensionButtonSerachResultSerializer(PensionNameSerializer):
    class Meta(PensionNameSerializer.Meta):
        fields = PensionNameSerializer.Meta.fields + (
            'pensionimages',
        )


class RoomButtonSearchResultSerializer(RoomBaseSerializer):
    pension = PensionButtonSerachResultSerializer(read_only=True)

    class Meta(RoomBaseSerializer.Meta):
        fields = RoomBaseSerializer.Meta.fields +(
            'pension',
        )
