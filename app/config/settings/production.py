from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

secrets = json.load(open(os.path.join(SECRET_DIR, 'produciton.json')))

ALLOWED_HOSTS = [
    'localhost',
]


DEFAULT_FILE_STORAGE = 'config.storages.S3DefaultStorage'
STATICFILES_STORAGE = 'config.storages.S3StaticStorage'


AWS_ACCESS_KEY_ID = secrets['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = secrets['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = secrets['AWS_STORAGE_BUCKET_NAME']
AWS_DEFAULT_ACL = secrets['AWS_DEFAULT_ACL']
AWS_S3_REGION_NAME = secrets['AWS_S3_REGION_NAME']
AWS_S3_SIGNATURE_VERSION = secrets['AWS_S3_SIGNATURE_VERSION']


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, '.static')


INSTALLED_APPS += [
    'storages',
]

secrets = json.load(open(os.path.join(SECRET_DIR, 'production.json')))

WSGI_APPLICATION = 'config.wsgi.production.application'

DATABASES = secrets['DATABASES']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
