from rest_framework import serializers
from ..models import  Room, RoomImage, Reservation

__all__ = (

    'RoomBaseSerializer',
    'RoomSerializer',
    'RoomReservationSerializer',
    'RoomImageSerializer',

    'Reservation',
)

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields=(
            'date'
        )


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = (
            # 'room',
            'room_image',
        )


class RoomBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = (
        # 'pension',
        'name' ,
        'size',
        'normal_num_poeple',
        'max_num_people' ,
        'price' ,
        )

class RoomSerializer(RoomBaseSerializer):
    roomimages = RoomImageSerializer(many=True, read_only=True)

    class Meta(RoomBaseSerializer.Meta):
        fields = RoomBaseSerializer.Meta.fields + (
        'structure' ,
        'equipments' ,
        'info',
        'roomimages',
        )

#
class RoomReservationSerializer(RoomBaseSerializer):
#     reservations=
#
#     class Meta(RoomBaseSerializer.Meta):
#         fields = RoomBaseSerializer.Meta.fields + (
#         'extra_charge_head' ,
#         'extra_charge_adult' ,
#         'extra_charge_child' ,
#         'extra_charge_baby',
#         'reservations',
#         )
    pass