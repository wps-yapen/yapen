from rest_framework import serializers
from ..models import Pension, Room, RoomImage, PensionImage

__all__ = (

    'RoomSerializer',
    'RoomImageSerializer',
)


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = (
            # 'room',
            'room_image',
        )


class RoomSerializer(serializers.ModelSerializer):
    roomimages = RoomImageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = (
        # 'pension',
        'name' ,
        'structure' ,
        'equipments' ,
        'info',
        'size',
        'normal_num_poeple',
        'max_num_people' ,
        'price' ,
        # 'extra_charge_head' ,
        # 'extra_charge_adult' ,
        # 'extra_charge_child' ,
        # 'extra_charge_baby' ,
        'roomimages',
        )