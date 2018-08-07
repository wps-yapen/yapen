from django.urls import path

from .views import PensionList, PensionDetail, PensionLocationList

urlpatterns = [
    path('pension/',
         PensionList.as_view(),
         name='PensionList'),
    path('pension/<str:sub_location_no>/',
         PensionLocationList.as_view(),
         name='PensionLocationList'),
    path('pension/<str:sub_location_no>/<int:pk>/',
         PensionDetail.as_view(),
         name='PensionList'),
]