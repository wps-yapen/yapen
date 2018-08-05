from django.urls import path

from .views import PensionList, PensionDetail

urlpatterns = [
    path('pension/',
         PensionList.as_view(),
         name='PensionList'),
    path('pension/<int:pk>/',
         PensionDetail.as_view(),
         name='PensionList'),
]