from django.urls import path


from reservation.apis import ReservationRoom, ReservationInfo, ReservationPay

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
]