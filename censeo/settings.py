# -*- coding: utf-8 -*-

import os
import sys

from django.core.urlresolvers import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = (
    'censeo',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'pipeline',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'censeo.context_processors.constants',
)
ROOT_URLCONF = 'censeo.urls'
WSGI_APPLICATION = 'censeo.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_COMPILERS = ('pipeline.compilers.less.LessCompiler',)
PIPELINE_YUGLIFY_BINARY = os.path.join(BASE_DIR, 'node_modules/.bin/yuglify')
PIPELINE_LESS_BINARY = os.path.join(BASE_DIR, 'node_modules/.bin/lessc')
PIPELINE_CSS = {
    'base': {
        'source_filenames': (
            'censeo/libs/bootstrap/css/bootstrap.css',
            'censeo/less/base.less',
        ),
        'output_filename': 'css/base.min.css',
    },
}
PIPELINE_JS = {
    'base': {
        'source_filenames': (
            'censeo/libs/jquery.maskedinput/jquery.maskedinput.js',
            'censeo/libs/bootstrap/js/bootstrap.js',
            'censeo/libs/underscore/underscore-min.js',
            'censeo/libs/backbone/backbone-min.js',
            'censeo/libs/jquery.cookie/jquery.cookie.js',
            'censeo/libs/jquery.csrf/jquery.csrf.js',
            'censeo/libs/spin.js/spin.js',
            'censeo/js/base.js',
        ),
        'output_filename': 'js/base.min.js',
    },
    'meet': {
        'source_filenames': (
            'censeo/js/meet.js',
        ),
        'output_filename': 'js/meet.min.js',
    }
}

# Registration
LOGIN_REDIRECT_URL = reverse_lazy('meet')
ACCOUNT_ACTIVATION_DAYS = 3

if 'runserver' in sys.argv:
    EMAIL_PORT = 1025
