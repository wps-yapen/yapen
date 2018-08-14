from rest_framework import serializers

from location.models import Room
from location.serializer.room import RoomBaseSerializer
from reservation.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Reservation
		fields = (
			'checkin_date',
			'checkout_date',
		)


class RoomReservationSerializer(RoomBaseSerializer):
	reservations = ReservationSerializer(many=True, read_only=True)
	class Meta(RoomBaseSerializer.Meta):
		fields = RoomBaseSerializer.Meta.fields + (
			'pk',
			'extra_charge_adult',
			'extra_charge_child',
			'extra_charge_baby',
			'status',
		)