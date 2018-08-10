from rest_framework import serializers

from .pension import PensionListSerializer
from ..models import Location, SubLocation

__all__ = (
    'SubLocationSerializer',
    'LocationSerializer',
)


class SubLocationSerializer(serializers.ModelSerializer):
    pensions = PensionListSerializer(many=True, read_only=True)

    class Meta:
        model = SubLocation
        fields =(
            'name',
            'sub_location_no',
            'pensions',
            'pensions_length'
        )


class LocationSerializer(serializers.ModelSerializer):
    sublocations = SubLocationSerializer(many=True, read_only=True)
    class Meta:
        model = Location
        fields =(
            'name',
            'sublocations',
            'pensions_length',
        )

