from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers

from .token import account_activation_token


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = '__all__'

    def to_internal_value(self, data):
        ret = super(UserSerializer, self).to_internal_value(data)

        return ret

    def to_representation(self, obj):
        ret = super(UserSerializer, self).to_representation(obj)
        return ret

    def validate_email(self, value):
        # if User.objects.filter(email=value).exists():
        #     raise serializers.ValidationError('이미 존재하는 이메일')
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('패스워드는 최소 8자 이상이어야 합니다.')
        return value

    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        user.active = False
        user.save()

        message = render_to_string('user/account_activate_email.html', {
            'user' : user,
            'domain' : 'localhost:8000',
            'uid' : urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8'),
            'token' : account_activation_token.make_token(user)
        })

        mail_subject = 'test'
        to_email= 'woodrand@naver.com'
        email = EmailMessage(mail_subject, message, to = [to_email,])
        email.send()

        return validated_data