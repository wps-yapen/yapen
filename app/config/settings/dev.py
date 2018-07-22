from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

secrets = json.load(open(os.path.join(SECRET_DIR, 'dev.json')))

ALLOWED_HOSTS = []

WSGI_APPLICATION = 'config.wsgi.dev.application'

DATABASES = secrets['DATABASES']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
