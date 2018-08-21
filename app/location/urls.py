from django.conf.urls import url
from django.urls import path

from .apis import PensionLocationNamesList, PensionDetail, PensionSubLocationList, PensionMainList

urlpatterns = [
    path('',
         PensionMainList.as_view(),
         name='PensionMainList'),
    path('location-name/',
         PensionLocationNamesList.as_view(),
         name='PensionLocationsList'),
    path('<str:sub_location_no>/',
         PensionSubLocationList.as_view(),
         name='PensionSubLocationList'),
    path('<str:sub_location_no>/<int:pk>/',
         PensionDetail.as_view(),
         name='PensionList'),
]