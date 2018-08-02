from django.conf import settings
from django.db import models


# pension image는 1장이라서 바로 pension모델의 속성으로 저장하고
# room에 속하는 image들은 따로 roomimage테이블 만들어서 foreingkey로 room과 연결함. many가 roomimage, one이 room

# Create your models here.
class Pension(models.Model):
    # 세부지역 메이페이지에서 크롤링할때 체우는 속성
    name = models.CharField(max_length=100) # '팬션이름'
    pension_image_thumbnail = models.ImageField(upload_to='pension', blank=True) # '팬션 이미지' # 해커톤때 photo # MEDIA_ROOT의세부경로가 upload_to에 들어감.
    lowest_price = models.IntegerField(default=0, blank=True) # '최저가'  # 해커톤때 price
    ypidx = models.IntegerField(default=0, blank=True) # '팬션별 고유번호'
    location = models.CharField(max_length=100, blank=True) #지역
    sub_location = models.CharField(max_length=100, blank=True)# 세부지역
    discount_rate = models.IntegerField(default=0,blank=True)# 할인률

    # pension-detail 페이지에서 크롤링해서 채우는 속성
    address = models.TextField(max_length=200, blank=True) # '주소'
    check_in = models.CharField(max_length=100,blank=True) # '입실시간'
    check_out = models.CharField(max_length=100,blank=True) # '퇴실시간'
    pickup = models.CharField(max_length=100,blank=True) # 픽업 여부
    room_num = models.IntegerField(default=0, blank=True)# '객실 수'  # 해커톤때 room
    info = models.TextField(blank=True)# '공지사항'
    theme = models.TextField(blank=True)# '테마' ----------> 이후에 view에서 json->list로 바꿔서 잘써야함.
    coordinate = models.TextField(blank=True) #좌표------->아직 크롤링 안했다.

    #pension-detail 페이지 하단부 이용안내 부분.
    check_in_out_detail = models.TextField(blank=True) # 입실/퇴실 시간 부연설명 간혹 있다.있으면 여기도 크롤링 해야함.
    pickup_detail = models.TextField(blank=True) # 픽업 가능 시 이부분도 크롤링 해야함.
    gretting = models.TextField(blank=True)# 팬션소개 및 인사말
    precautions = models.TextField(blank=True)# 이용 주의사항



# 팬션, 방 이미지 어떻게 관리하는지?
# pension ->  pension_image_thumbnail이미지 한장 mainpage 크롤링할때 가져오기.
#         ->  PensionImage 모델괴 Foreignkey로 연결되서 여러장의 pension이미지를 table로 가짐.
# room    ->  RoomImage 모델괴 Foreignkey로 연결되서 여러장의 room이미지를 table로 가짐.

class Room(models.Model):
    pension = models.ForeignKey( Pension, on_delete=models.CASCADE)

    name = models.CharField(max_length=100) # '객실 명'
    structure = models.CharField(max_length=100,blank=True) # '객실구조'
    equipments = models.TextField(blank=True) # '구비시설'
    info = models.TextField(blank=True) # '객실설명'
    size = models.CharField(max_length=100,blank=True) # '크기'
    normal_num_poeple = models.IntegerField(default=0,blank=True) # '기준인원'
    max_num_people = models.IntegerField(default=0,blank=True) # '최대인원'
    price = models.IntegerField(default=0,blank=True) # '가격'

    # 추가요금안내
    # '인원추가 불가능' 시에는 여기 그대로 넣고 if문으로 아예 아래는 값 대입하지 말자.
    extra_charge_head = models.CharField( max_length=100,blank=True)
    extra_charge_adult = models.IntegerField(default=0,blank=True)
    extra_charge_child = models.IntegerField(default=0,blank=True)
    extra_charge_baby = models.IntegerField(default=0,blank=True)


class PensionImage(models.Model):
    pension = models.ForeignKey(Pension,on_delete=models.CASCADE,)
    pension_image = models.ImageField(upload_to='pension', blank=True) # '팬션 이미지'


class RoomImage(models.Model):
    room= models.ForeignKey(Room,on_delete=models.CASCADE,)
    room_image = models.ImageField(upload_to='room', blank=True) # '방 이미지'


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
