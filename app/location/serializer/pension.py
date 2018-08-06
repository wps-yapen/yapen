from rest_framework import serializers

from .room import RoomSerializer
from ..models import Pension,PensionImage

__all__ = (
    'PensionListSerializer',
    'PensionDetailSerializer',
    'PensionImageSerializer',

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

