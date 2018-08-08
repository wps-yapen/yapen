from django.urls import path

from .views import SignUp, UserActivate, UserDetailView, AuthToken, UserChangePassword, Deletetoken

app_name = 'members'

urlpatterns = [
    path('activate/<str:uidb64>/<str:token>', UserActivate.as_view(), name='activate'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', AuthToken.as_view(), name='login'),
    path('detail/', UserDetailView.as_view(), name='detail'),
    path('changepassword/', UserChangePassword.as_view(), name='changepassword'),
    path('logout/', Deletetoken.as_view(), name='logout'),

]
