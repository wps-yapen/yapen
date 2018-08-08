from django.conf import settings
from django.db import models

from location.models import Room


class Reservation(models.Model):
  room = models.ForeignKey(Room,related_name='reservations', on_delete=models.CASCADE)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  checkin_date = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True)
  checkout_date = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True)

  # 예약페이지 상세정보
  subscriber = models.CharField( max_length=100,blank=True) # 예약자 이름
  phone_number = models.CharField( max_length=100,blank=True) # 휴대폰 번호
  birth_date = models.CharField( max_length=100,blank=True) # 생년월일19920803
  pickup_or_not = models.BooleanField(default=True, blank=True) #픽업여부
  entering_time = models.CharField( max_length=100,blank=True) # 입실예정시간
  requested_term = models.TextField(blank=True) # 요청사항

  # 결제방법 - > 무통장 입금 관련 정보
  deposit_bank = models.CharField( max_length=100,blank=True) # 입금은행
  depositor_name = models.CharField( max_length=100,blank=True) # 입금자명