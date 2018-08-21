import traceback

from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from members.serializer import UserCreateSerializer, UserDetailSerializer, UserPasswordChange, FacebookUserSerializer
from members.token import account_activation_token

User = get_user_model()


class SignUp(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        # return Response('유효성 검사에 실패하였습니다', status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
                user.is_active = True
                user.save()
                return Response(user.email + '계정이 활성화 되었습니다. ', status=status.HTTP_200_OK)
            else:
                return Response('만료된 링크입니다.', status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(traceback.format.exc())


# login
class AuthToken(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)

            data = {
                'token': token.key,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return AuthenticationFailed()


class UserChangePassword(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def patch(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        serializer = UserPasswordChange(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response('비밀번호가 변경되었습니다.', status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class Deletetoken(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class FacebookLogin(APIView):
    def post(self, request):
        facebook_id = request.data.get('facebook_id')
        last_name = request.data.get('last_name')
        first_name = request.data.get('first_name')
        user, __ = User.objects.get_or_create(
            username=facebook_id,
            defaults={
                'last_name': last_name,
                'first_name': first_name,
            }
        )

        token, __ = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'user': FacebookUserSerializer(user).data
        }
        return Response(data)
