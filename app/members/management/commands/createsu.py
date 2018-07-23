import json
import os
from django.contrib.auth.hashers import check_password, make_password

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from django.conf import settings

# admin / 특정비밀번호
# 위 값으로 로그인 시도 시 authenticate가 성공하도록 커스텀 Backend를 작성
# members.backends모듈에 작성
# Backend명은 SettingsBackend


User = get_user_model()


secrets = json.load(open(os.path.join(settings.SECRET_DIR, 'base.json')))

class Command(BaseCommand):
    def handle(self, *args, **options):
        secrets = json.load(open(os.path.join(settings.SECRET_DIR, 'base.json')))
        if not User.objects.filter(username=secrets['SUPERUSER_USERNAME']).exists():
            User.objects.create_superuser(
                username=secrets['SUPERUSER_USERNAME'],
                password=secrets['SUPERUSER_PASSWORD'],
                email=secrets['SUPERUSER_EMAIL'],
            )

