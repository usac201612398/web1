"""

Django settings for web1 project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/

"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start developmen    t settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-i%35q9sc8q^vah@$-wnd@mgjy&ct3kpf=(8x_)l=rsxrzy=ad_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
SECURE_CROSS_ORIGIN_OPENER_POLICY = None
#ALLOWED_HOSTS = ['popoyan.com.gt','sdc-iot.popoyan.com.gt','www.sdc-iot.popoyan.com.gt']
ALLOWED_HOSTS = ['sdc-iot.popoyan.com.gt']
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'web1/data/static')]
# Application definition
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO','https')
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
#    'django.contrib.sites',
    'app1',
    'ejemplo',
    'django_auth_adfs',
]

#SITE_ID = 1
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django_auth_adfs.middleware.LoginRequiredMiddleware',
]

CUSTOM_FAILED_RESPONSE_VIEW = 'dot.path.to.custom.views.login_failed'
ROOT_URLCONF = 'web1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'data/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
#		'django_auth_adfs.context_processors.adfs_url',
#                'microsoft_auth.context_processors.microsoft',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
#        'djanto.contrib.auth.backends.ModelBackend',
	'django_auth_adfs.backend.AdfsAuthCodeBackend',
]

client_id = 'd27b7533-221a-4742-b79d-9450ff8ffe26'
client_secret =  '0Rj8Q~.0DAXFskEPZtfM~~FwXAp7lFzHifz6Ib1n'
tenant_id = '2e932f25-355e-45b3-bd8b-764aaf3fd625'

AUTH_ADFS = {

    'AUDIENCE': client_id,
    'CLIENT_ID': client_id,
    'CLIENT_SECRET': client_secret,
    'CLAIM_MAPPING': {'first_name': 'given_name',
                      'last_name': 'family_name',
                      'email': 'upn'},
    'GROUPS_CLAIM': 'roles',
    'MIRROR_GROUPS': True,
    'USERNAME_CLAIM': 'upn',
    'TENANT_ID': tenant_id,
    'RELYING_PARTY_ID': client_id,
}

WSGI_APPLICATION = 'web1.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sdc',
        'PASSWORD': '1234',
        'USER': 'postgres',
        'PORT': '',
        'HOST': 'localhost'
    },

#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    },

    
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

LOGIN_URL = 'django_auth_adfs:login'
# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LOGIN_REDIRECT_URL = '/'


# URL base del servidor ADFS para cerrar sesión
ADFS_LOGOUT_URL = 'https://sdc-iot.popoyan.com.gt/adfs/ls/?wa=wsignout1.0'
LOGOUT_REDIRECT_URL = '/app1/homepage'


# URL a la que ADFS debe redirigir después de cerrar sesión

ADFS_LOGOUT_URL = 'https://sdc-iot.popoyan.com.gt/adfs/ls/?wa=wsignout1.0'
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Guatemala'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,"static/")
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

