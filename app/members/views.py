import traceback

from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.compat import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from rest_framework.views import APIView

from members.serializer import UserCreateSerializer, UserDetailSerializer, UserPasswordChange
from members.token import account_activation_token

User = get_user_model()


class SignUp(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserActivate(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64.encode('utf-8')))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoseNotExist):
            user = None


        try:
            if user is not None and account_activation_token.check_token(user, token):
                user.active = True
                user.save()
                return Response(user.email + '계정이 활성화 되었습니다. ', status=status.HTTP_200_OK)
            else:
                return Response('만료된 링크입니다.', status = status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(traceback.format.exc())

class AuthToken(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            token, _= Token.objects.get_or_create(user=user)

            data = {
                'token' : token.key,

            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return AuthenticationFailed()


class UserDetailView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    def get(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePassword(APIView):
    permission_classes = (
    permissions.IsAuthenticated,
    )

    def patch(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        serializer = UserPasswordChange(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)




