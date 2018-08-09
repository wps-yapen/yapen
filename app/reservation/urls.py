from django.urls import path


from reservation.views import ReservationRoom, ReservationPay

urlpatterns = [
    path('<int:pk>/<str:date>/',
         ReservationRoom.as_view(),
         name='Reservation'),
    path('<int:pk>/<str:date>/info/',
         ReservationPay.as_view(),
         name='ReservationPay'),
]