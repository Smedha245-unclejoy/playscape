"""
Django settings for PlayYourWay project.

Generated by 'django-admin startproject' using Django 1.11.13.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import django_heroku
import dj_database_url
from decouple import config
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = '%3lf=i+-i$1uq9i*lfaj%&mbvu9z+=9#r1uh0_90wt_6l@klro'



# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['127.0.0.1','playscape.herokuapp.com']
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "playscape.settings")

#application = get_wsgi_application()
#application = DjangoWhiteNoise(application)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'rest_framework',
    'rest_framework_gis',
    'rest_framework.authtoken',
    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',
    'sportsapp',
    'posts',
    'likes',
    'friends',
    'sports',
    'storages',
    'playground',
    'events'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'PlayYourWay.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]
#'django.core.context_processors.static',
STATICFILES_FINDERS = (
     'django.contrib.staticfiles.finders.FileSystemFinder',
     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

WSGI_APPLICATION = 'PlayYourWay.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
#'default': {
#    "ENGINE": "django.contrib.gis.db.backends.postgis",
#    "NAME": "postgres",
#    "USER": "postgres",
#    'CONN_MAX_AGE': 500,
#}
#DATABASES = {
#    'default':dj_database_url.config(default='postgres://dwqeaybsooqrvg:6461bd5d2a40933e56c31cf404c80d8c8aa2a2a3b981dd2d6193aed585e00457@ec2-79-125-110-209.eu-west-1.compute.amazonaws.com:5432/dabi90igcm1s9l')
#}
#DATABASES['default'] = dj_database_url.config()
DATABASES = {
     'default' : dj_database_url.config()
}
#db_from_env = dj_database_url.config(default=os.getenv('DATABASE_URL'))
#DATABASES['default'].update(db_from_env)
DATABASES['default']['ENGINE']='django.contrib.gis.db.backends.postgis'
print(DATABASES['default'])
if 'DATABASE_URL' in os.environ:  # please help me heroku gods
    if 'postgres' in os.environ['DATABASE_URL']:
        os.environ['DATABASE_URL'] = os.environ['DATABASE_URL'].replace('postgres', 'postgis')
#if os.getenv('DYNO'):
#    DATABASES['default'] =  dj_database_url.parse(os.getenv('DATABASE_URL'),'django.contrib.gis.db.backends.postgis')
#    print(DATABASES['default'])

#DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
DATABASES['default']['NAME'] = 'postgres'
DATABASES['default']['USER'] = 'postgres'


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}

AUTHENTICATION_BACKENDS = (
    # ...
    'rest_framework_social_oauth2.backends.DjangoOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    # Facebook OAuth2
    'social_core.backends.facebook.FacebookAppOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
)
# Facebook configuration
SOCIAL_AUTH_FACEBOOK_KEY = '1167675320041732'
SOCIAL_AUTH_FACEBOOK_SECRET = '7e10dadc3976fe17b5e26ab07d5c3078'

# Define SOCIAL_AUTH_FACEBOOK_SCOPE to get extra permissions from facebook. Email is not sent by default, to get it, you must request the email permission:
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email','user_gender','user_friends','public_profile']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id,name,email'
}
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY ='515382694363-fsq3de6t2uieh55vsh9pj95tb8kt4oh6.apps.googleusercontent.com'  #Paste CLient Key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'z4CmIwh5jATA1uiXBJdb2s3N' #Paste Secret Key
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email','gender','name']
SOCIAL_AUTH_GOOGLE_OAUTH2_PROFILE_EXTRA_PARAMS = {'fields': 'name,email,gender'}
OAUTH2_PROVIDER = {
        'ACCESS_TOKEN_EXPIRE_SECONDS': 60 * 60 * 24,
 }


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True
DEFAULT_FROM_EMAIL='priti7608@gmail.com'
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER='priti7608@gmail.com'
EMAIL_HOST_PASSWORD='priti@7608'
EMAIL_USE_TLS=True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#STATIC_URL = '/static/'
# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'PlayYourWay/static'),
)
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
AWS_ACCESS_KEY_ID = 'AKIAIZZLM3PD4Z7HSOGA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'piptc-static'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_LOCATION = 'static'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

DEFAULT_FILE_STORAGE = 'PlayYourWay.storage_backends.MediaStorage'
#For storing images and other files
#ENV_PATH = os.path.abspath(os.path.dirname(__file__))
#MEDIA_ROOT = os.path.join(ENV_PATH, 'media/')
#print("base dir path", BASE_DIR)
#print("env dir path", ENV_PATH)
#MEDIA_URL = 'media/'
django_heroku.settings(locals())
GEOS_LIBRARY_PATH = os.getenv('GEOS_LIBRARY_PATH')
GDAL_LIBRARY_PATH = os.getenv('GDAL_LIBRARY_PATH')
