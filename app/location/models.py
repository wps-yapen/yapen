from django.conf import settings
from django.db import models


# pension image는 1장이라서 바로 pension모델의 속성으로 저장하고
# room에 속하는 image들은 따로 roomimage테이블 만들어서 foreingkey로 room과 연결함. many가 roomimage, one이 room

# Create your models here.
class Pension(models.Model):
    name = models.CharField(max_length=100) # '팬션이름'
    # pension_list에서 보이는 사진 1장 / media 부터의 경로가 url로 표시됨. 해커톤때는 웹상의 절대경로 저장해줬음.
    pension_image_thumbnail = models.ImageField(upload_to='pension', blank=True) # '팬션 이미지' # 해커톤때 photo
    lowest_price = models.CharField(max_length=100) # '최저가'  # 해커톤때 price
    address = models.TextField(max_length=100, blank=True) # '주소'
    # location = models.CharField(max_length=100, blank=True)
    # sub_location= models.CharField(max_length=100, blank=True)
    check_in = models.CharField(max_length=100,blank=True) # '입실시간'
    check_out = models.CharField(max_length=100,blank=True) # '퇴실시간'
    room_num = models.CharField(max_length=100,blank=True)# '방갯수'  # 해커톤때 room
    info = models.TextField(max_length=100,blank=True)# '정보'
    theme = models.CharField(max_length=100,blank=True)# '테마'
    pldx = models.IntegerField() # '팬션별 고유번호'

    # 추가적으로 이미지 save하는 함수 여기 넣어주고싶다.


class Room(models.Model):
    pension = models.ForeignKey( Pension, on_delete=models.CASCADE)
    name = models.CharField(max_length=100) # '방 이름'
    size = models.CharField(max_length=100,blank=True) # '방 사이즈'
    number_of_people = models.CharField(max_length=100,blank=True) # '수용인원'
    price = models.CharField( max_length=100,blank=True) # '가격'


class RoomImage(models.Model):
    room_id = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
    )
    room_image = models.ImageField(upload_to='room', blank=True) # '방 이미지'

    # 추가적으로 이미지 save하는 함수 여기 넣어주고싶다.



# 반대쪽 입장에서 이것이 뭔지 생각해서 related_name 정한다.
class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True)


class Comment(models.Model):
    pension = models.ForeignKey(
        Pension,
        on_delete=models.CASCADE,
        null=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    content = models.CharField(max_length=300, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PensionLike(models.Model):
    pension = models.ForeignKey(
        Pension,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
