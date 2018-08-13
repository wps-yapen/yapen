from django.urls import path


from reservation.views import ReservationRoom, ReservationInfo

urlpatterns = [
    path('<int:pk>/<str:date>/',
         ReservationRoom.as_view(),
         name='Reservation'),
    path('info/',
         ReservationInfo.as_view(),
         name='ReservationPay'),
]