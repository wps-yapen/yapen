from rest_framework import serializers


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

class RoomSerializer(RoomBaseSerializer):
    roomimages = RoomImageSerializer(many=True, read_only=True)

    class Meta(RoomBaseSerializer.Meta):
        fields = RoomBaseSerializer.Meta.fields + (
        'structure' ,
        'equipments' ,
        'info',
        'roomimages',
        )
