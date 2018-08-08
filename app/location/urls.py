from django.urls import path

from .views import PensionLocationsList, PensionDetail, PensionSubLocationList

urlpatterns = [
    path('',
         PensionLocationsList.as_view(),
         name='PensionList'),
    path('<str:sub_location_no>/',
         PensionSubLocationList.as_view(),
         name='PensionLocationList'),
    path('<str:sub_location_no>/<int:pk>/',
         PensionDetail.as_view(),
         name='PensionList'),
]