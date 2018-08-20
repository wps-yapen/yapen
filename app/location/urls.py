from django.conf.urls import url
from django.urls import path

from .views import PensionLocationNamesList, PensionDetail, PensionSubLocationList, PensionMainList, IosPensionMainList, \
    IosPensionSubLocationList

urlpatterns = [
    path('',
         PensionMainList.as_view(),
         name='PensionMainList'),
    path('location-name/',
         PensionLocationNamesList.as_view(),
         name='PensionLocationsList'),

    # IOS 요청으로 예비로 만들어놈.@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    path('ios/', IosPensionMainList.as_view(),
         name='IosPensionMainList'),
    path('ios/<str:sub_location_no>/', IosPensionSubLocationList.as_view(),
         name='IosPensionLocationsList'),
    # IOS 요청으로 예비로 만들어놈.@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


    path('<str:sub_location_no>/',
         PensionSubLocationList.as_view(),
         name='PensionSubLocationList'),
    path('<str:sub_location_no>/<int:pk>/',
         PensionDetail.as_view(),
         name='PensionList'),

]