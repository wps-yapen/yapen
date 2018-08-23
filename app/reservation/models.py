from django.conf import settings
from django.db import models

from location.models import Room

class Reservation(models.Model):
  room = models.ForeignKey(Room,related_name='reservations', on_delete=models.CASCADE)
  user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='reservations', on_delete=models.CASCADE)
  checkin_date = models.DateField(auto_now=False, auto_now_add=False, blank=True)
  checkout_date = models.DateField(auto_now=False, auto_now_add=False, blank=True)
  total_price = models.IntegerField(default=0, blank=True)

  #예약번호 번호
  reservation_num = models.CharField( max_length=100,blank=True)

  # 예약페이지 상세정보
  subscriber = models.CharField( max_length=100,blank=True) # 예약자 이름
  phone_number = models.CharField( max_length=100,blank=True) # 휴대폰 번호
  # birth_date = models.CharField( max_length=100,blank=True) # 생년월일19920803
  # pickup_or_not = models.BooleanField(default=True, blank=True) #픽업여부
  # entering_time = models.CharField( max_length=100,blank=True) # 입실예정시간
  # requested_term = models.TextField(blank=True) # 요청사항

  # 결제방법
  method_of_payment = models.CharField( max_length=100,blank=True)

  # 무통장입금이라면?
  deposit_bank = models.CharField( max_length=100,blank=True) # 입금은행
  depositor_name = models.CharField( max_length=100,blank=True) # 입금자명

  # 카드간편결제라면?
  card_number = models.CharField( max_length=100,blank=True) # 카드번호
  expiration_month =  models.CharField( max_length=100,blank=True)  # 유효기간 월
  expiration_year =  models.CharField( max_length=100,blank=True) #유효기간 년
  card_password = models.CharField( max_length=100,blank=True) # 카드 비밀번호
  card_type = models.CharField( max_length=100,blank=True) # 카드구분
  birth_date_of_owner = models.CharField( max_length=100,blank=True) # 생년월일19920803
  installment_plan = models.CharField( max_length=100,blank=True) # 할부선택
  email = models.EmailField(blank=True)

  def __str__(self):
    return f'{self.user}: {self.room} 총 가격:{self.total_price}'
