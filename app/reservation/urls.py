from django.urls import path


from reservation.apis import ReservationRoom, ReservationInfo, ReservationPay, ReservationSearchByReservation_num, \
    ReservationSearchByInfo

urlpatterns = [
    path('<int:pk>/<str:date>/',
         ReservationRoom.as_view(),
         name='Reservation'),
    path('info/',
         ReservationInfo.as_view(),
         name='ReservationInfo'),
    path('pay/',
         ReservationPay.as_view(),
         name='ReservationPay'),
    path('ReservationSearchByReservation_num/',
         ReservationSearchByReservation_num.as_view(),
         name='ReservationSearchByReservation_num'),
    path('ReservationSearchByInfo/',
         ReservationSearchByInfo.as_view(),
         name='ReservationSearchByInfo')
]