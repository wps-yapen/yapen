from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .token import account_activation_token


User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = '__all__'

    def to_internal_value(self, data):
        ret = super(UserCreateSerializer, self).to_internal_value(data)

        return ret

    def to_representation(self, obj):
        ret = super(UserCreateSerializer, self).to_representation(obj)
        return ret


    def validate_email(self, value):
        return value


    def validate_password(self, value):

        if len(value) < 8:
            raise serializers.ValidationError('패스워드는 최소 8자 이상이어야 합니다.')
        return value

    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            password = validated_data['password'],
            email = validated_data['email'],
            phone_number = validated_data['phone_number'],
        )
        user.set_password(validated_data['password'])

        user.active = False
        user.save()

        message = render_to_string('user/account_activate_email.html', {
            'user' : user,
            'domain' : 'localhost:8000',
            'uid' : urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8'),
            'token' : account_activation_token.make_token(user)
        })

        mail_subject = '회원가입 메일입니다.'
        to_email= user.email
        email = EmailMessage(mail_subject, message, to = [to_email,])
        email.send()

        return validated_data


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]


class UserPasswordChange(serializers.ModelSerializer):
    password = serializers.CharField()
    password2 = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'password',
            'password2',
        )

    def validate_password(self, password):
        # 두개의 비밀번호가 일치하는지 검사
        # 일치하면 비밀번호 유효성 검사 실시

        password2 = self.initial_data.get('password2')
        if not password == password2:
            raise serializers.ValidationError('비밀번호가 일치하지 않습니다.')

        errors = dict()

        try:
            validate_password(password=password)

        except ValidationError as e:
            errors['password'] = list(e.messages)
            print(errors)

        if errors:
            raise serializers.ValidationError(errors)

        return password

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        print('1',validated_data)
        instance.save()

        return instance



