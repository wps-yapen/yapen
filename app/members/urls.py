from django.urls import path

from .views import SignUp, UserActivate, LoginApiView

app_name = 'members'
urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('activate/<str:uidb64>/<str:token>', UserActivate.as_view(), name='activate'),
]
