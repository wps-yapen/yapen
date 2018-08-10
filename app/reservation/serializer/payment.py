
import datetime

from location.models import Room
from members.models import User
from reservation.models import Reservation
from reservation.serializer.reservation import ReservationSerializer


class ReservationPaySerializer(ReservationSerializer):
	class Meta(ReservationSerializer):

		fields = ReservationSerializer.Meta.fields + (
			'room',
			'user',
			'checkin_date',
			'checkout_date',
			'reservation_price',
		)


	def create(self,validated_data):
		list1 = validated_data['checkin_date'].split('-')
		year = int(list1[0])
		month = int(list1[1])
		day = int(list1[2])
		target_date1 = datetime.date(year, month, day)
		list2 = validated_data['checkout_date'].split('-')
		year = int(list2[0])
		month = int(list2[1])
		day = int(list2[2])
		target_date2 = datetime.date(year, month, day)
		reservation = Reservation.objects.create(
			room = Room.objects.get(pk=int(validated_data['room'])),
			user = User.objects.get(pk=int(validated_data['user'])),
			checkin_date = target_date1,
			checkout_date = target_date2,
			reservation_price = int(validated_data['reservation_price'])
		)
		return validated_data

# import datetime
#
# from location.models import Room
# from members.models import User
# from reservation.models import Reservation
# from reservation.serializer.reservation import ReservationSerializer
#
#
# class ReservationPaySerializer(ReservationSerializer):
# 	class Meta(ReservationSerializer):
#
# 		fields = ReservationSerializer.Meta.fields + (
# 			'room',
# 			'user',
# 			'checkin_date',
# 			'checkout_date',
# 			'reservation_price',
# 		)
# 	def create(self,validated_data):
# 		list1 = validated_data['checkin_date'].split('-')
# 		year = int(list1[0])
# 		month = int(list1[1])
# 		day = int(list1[2])
# 		target_date1 = datetime.date(year, month, day)
# 		list2 = validated_data['checkout_date'].split('-')
# 		year = int(list2[0])
# 		month = int(list2[1])
# 		day = int(list2[2])
# 		target_date2 = datetime.date(year, month, day)
# 		reservation = Reservation.objects.create(
# 			room = Room.objects.get(pk=int(validated_data['room'])),
# 			user = User.objects.get(pk=int(validated_data['user'])),
# 			checkin_date = target_date1,
# 			checkout_date = target_date2,
# 			reservation_price = int(validated_data['reservation_price'])
# 		)
# 		return validated_data
