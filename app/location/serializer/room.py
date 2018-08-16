from rest_framework import serializers

# from location.serializer.pension import PensionButtonSerachResultSerializer
from ..models import  Room, RoomImage

__all__ = (

    'RoomBaseSerializer',
    'RoomSerializer',
    'RoomImageSerializer',
)

class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = (
            'room_image',
        )

class RoomBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
        'pk',
        'name' ,
        'size',
        'normal_num_poeple',
        'max_num_people' ,
        'price' ,
        )

# Pension detail 페이지에서 각 room 상세정보 보여줄 serializer
class RoomSerializer(RoomBaseSerializer):
    roomimages = RoomImageSerializer(many=True, read_only=True)

    class Meta(RoomBaseSerializer.Meta):
        fields = RoomBaseSerializer.Meta.fields + (
        'structure' ,
        'equipments' ,
        'info',
        'roomimages',
        )

