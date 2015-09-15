import os.path

DEBUG = True

TEMPLATE_DEBUG = DEBUG

PROJECT_DIR = os.path.dirname(__file__)

ADMINS = (
    ('Mariano Falcon', 'mf2286@gmail.com'),
)

MANAGERS = ADMINS

AUTH_PROFILE_MODULE = "finance.UserProfile"

import sys


#if 'test' in sys.argv:
#    DATABASES['default'] = {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': 'testdb'
#    }


TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'es-ar'

DATE_FORMAT = 'Y-m-d'
USE_I18N = True
USE_L10N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(PROJECT_DIR, 'staticfiles')

# Additional locations of static files
STATICFILES_DIRS = (os.path.join(PROJECT_DIR, 'static/'),)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'v1qjnn09%khqqf&z63-!*lniczmike9b87=avu^=xn6+adkqwd'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'tenant_schemas.middleware.TenantMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
FIXTURE_DIRS = (
   os.path.join(PROJECT_DIR, 'fixtures'),
)

ROOT_URLCONF = 'edujango.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

SHARED_APPS = (
    'django.contrib.auth',  
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.comments',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'south',
    'registration',
    'easy_pdf',
    'tinymce',
    'students',
    'finance',
    'efinance',
    'eventos',
    'college',
    'tagging', #blog
    'mptt', #blog
    'zinnia', #blog
    'schedule', #Calendario
    'tenant_schemas',
    'bootstrap3',
    'jardin',
    'crispy_forms',
    
)

TENANT_APPS = (
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'students',
    'finance',
    'efinance',
    'eventos',
    'college',
    'tagging', #blog
    'mptt', #blog
    'zinnia', #blog
    'schedule', #Calendario
    'tenant_schemas',
    'bootstrap3',
    'jardin',
    'south',
    'crispy_forms',
   
)

INSTALLED_APPS = SHARED_APPS + TENANT_APPS + ('tenant_schemas',)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

SOUTH_DATABASE_ADAPTERS = {
    'default': 'south.db.postgresql_psycopg2',
}

TENANT_MODEL = "efinance.Client"

SITE_ID = 1


LOGIN_REDIRECT = '/app/'
LOGIN_REDIRECT_URL = '/app/'

ACCOUNT_ACTIVATION_DAYS = 5
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'mf2286@gmail.com'
EMAIL_HOST_PASSWORD = 'maf99cneaxxx'
EMAIL_PORT = 587

DEFAULT_CHARSET = 'utf-8'

TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace",
    'theme': "advanced",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    'theme_advanced_toolbar_location' : "top",
}
TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True


TEMPLATE_CONTEXT_PROCESSORS = (
  'django.contrib.auth.context_processors.auth',
  'django.core.context_processors.i18n',
  'django.core.context_processors.request',
  'zinnia.context_processors.version', 
  'django.core.context_processors.static',
)


AUTH_USER_MODEL = 'finance.CustomUser'


try:
    from dev_settings import *
except:
    from prod_settings import *

