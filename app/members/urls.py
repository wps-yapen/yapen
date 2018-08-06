from django.urls import path

from .views import SignUp, UserActivate, UserDetailView

app_name = 'members'

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('activate/<str:uidb64>/<str:token>', UserActivate.as_view(), name='activate'),
    path('detail/', UserDetailView.as_view(), name='detail'),
]
