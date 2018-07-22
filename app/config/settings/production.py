from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
]

secrets = json.load(open(os.path.join(SECRET_DIR, 'production.json')))

WSGI_APPLICATION = 'config.wsgi.production.application'

DATABASES = secrets['DATABASES']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
