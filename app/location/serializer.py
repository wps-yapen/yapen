from rest_framework import serializers
from .models import Pension, Room, RoomImage, PensionImage

__all__ = (
    'PensionListSerializer',
    'PensionDetailSerializer',
    'PensionImageSerializer',
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


class PensionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PensionImage
        fields = (
            # 'pension',
            'pension_image',
        )


# Mainpage에서 보여줄 field 들만 serializer하는
class PensionBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pension
        fields =(
            'pk',
            'name',
            'pension_image_thumbnail',
            'lowest_price',
            'discount_rate',
        )


class PensionListSerializer(PensionBaseSerializer):
    pass


class PensionDetailSerializer(PensionBaseSerializer):
    rooms = RoomSerializer(many=True, read_only=True)
    pensionimages = PensionImageSerializer(many=True, read_only=True)

    class Meta(PensionBaseSerializer.Meta):
        fields = PensionBaseSerializer.Meta.fields + (
            'location',
            'sub_location',
            'address',
            'check_in',
            'check_out',
            'pickup',
            'room_num',
            'info',
            'theme',
            'lat',
            'lng',
            'check_in_out_detail',
            'pickup_detail',
            'gretting',
            'precautions',

            'pensionimages',
            'rooms',
        )


