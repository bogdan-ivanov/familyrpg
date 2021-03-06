# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print 'PROJECT_PATH', PROJECT_PATH
print 'BASE_DIR', BASE_DIR


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^&zksvq1gn%-5lb4=1b0(z3coiq_nvao=v9n9lkjj6agnflr96'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'familyquest',
    'tastypie',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'familyrpg.urls'

WSGI_APPLICATION = 'familyrpg.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'familyrpg',
        'USER': 'postgres',
        'PASSWORD': 'iddqdidkfa',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'OPTIONS': {'autocommit': True,},
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

#STATIC_ROOT = ''

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, "familyrpg", "static"),
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, "familyrpg", "templates"),
)
UPLOAD_DIR = os.path.join(PROJECT_PATH, "familyrpg", "static"),