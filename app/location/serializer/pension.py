from rest_framework import serializers

from location.serializer.room import RoomSerializer
from ..models import Pension,PensionImage

__all__ = (
    'PensionListSerializer',
    'PensionDetailSerializer',
    'PensionImageSerializer',
    'PensionNameSerializer',

)


class PensionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PensionImage
        fields = (
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
            'lat',
            'lng',
        )

class PensionListSerializer(PensionBaseSerializer):
    pass


class PensionDetailSerializer(PensionBaseSerializer):
    rooms = RoomSerializer(many=True, read_only=True)
    pensionimages = PensionImageSerializer(many=True, read_only=True)

    class Meta(PensionBaseSerializer.Meta):
        fields = PensionBaseSerializer.Meta.fields + (
            'address',
            'check_in',
            'check_out',
            'pickup',
            'room_num',
            'info',
            'theme',
            'check_in_out_detail',
            'pickup_detail',
            'gretting',
            'precautions',

            'pensionimages',
            'rooms',
        )

class PensionNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pension
        fields = (
            'pk',
            'name',
        )