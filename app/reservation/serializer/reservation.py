import re

from rest_framework import serializers

from location.models import Room
from location.serializer.pension import PensionNameSerializer
from location.serializer.room import RoomBaseSerializer

from reservation.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Reservation
		fields = (
			'pk',
			'checkin_date',
			'checkout_date',
		)


class RoomReservationSerializer(RoomBaseSerializer):
	# reservations = ReservationSerializer(many=True, read_only=True)
	class Meta(RoomBaseSerializer.Meta):
		fields = RoomBaseSerializer.Meta.fields + (
			'pk',
			'extra_charge_adult',
			'extra_charge_child',
			'extra_charge_baby',
			'status',
			# 'reservations',
		)

class PensionReservationSerializer(PensionNameSerializer):

	rooms = RoomReservationSerializer(many=True, read_only=True)

	def to_representation(self, instance):
		"""Convert `username` to lowercase."""
		ret = super().to_representation(instance)

		address =ret['address']
		result = re.findall('지번 : (.*) ', address)
		ret['address'] = result
		return ret


	class Meta(PensionNameSerializer.Meta):
		fields = PensionNameSerializer.Meta.fields + (
			''
			'address',
			'rooms'
		)

