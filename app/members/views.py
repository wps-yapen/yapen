import traceback

from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import status, permissions
from rest_framework.response import Response

from rest_framework.views import APIView

from members.serializer import UserSerializer
from members.token import account_activation_token

User = get_user_model()

class SignUp(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
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



