from rest_framework import serializers

from .pension import PensionListSerializer
from ..models import Location, SubLocation

__all__ = (
    'SubLocationSerializer',
    'LocationSerializer',
)

# 검색창에서 쓰이는 Locaiton, SubLocation 의 name, location_no, pension수 보이기 위한 serailzier
class SubLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubLocation
        fields =(
            'name',
            'pensions_length',
            'sub_location_no',

        )


class LocationSerializer(serializers.ModelSerializer):
    sublocations = SubLocationSerializer(many=True, read_only=True)
    class Meta:
        model = Location
        fields =(
            'name',
            'pensions_length',
            'sublocations',

        )

