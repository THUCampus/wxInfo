# Django settings for TsinghuaChat project.
import os
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     
)

MANAGERS = ADMINS

if 'SERVER_SOFTWARE' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'qYWIejIojQUXFCAUnVzY',        # Or path to database file if using sqlite3.
            'USER': 'i9m2l3f4Rm10DAVhYrfrW86f',                      # Not used with sqlite3.
            'PASSWORD': '339gRvGZ7AIgDaA88aD10SG7tLYNQbn0',                  # Not used with sqlite3.
            'HOST': 'sqld.duapp.com',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '4050',                      # Set to empty string for default. Not used with sqlite3.
            }
    }
elif (os.environ.get('USER', '') == 'ssastadmin') or ('SSAST_DEPLOYMENT' in os.environ):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'tuantuan',
            'USER': 'tuantuan',
            'PASSWORD': '8G5weIMsCphP87XA',
            'HOST': '',
            'PORT': '',
            }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'
            'NAME': 'tuantuan',        # Or path to database file if using sqlite3.
            'USER': 'root',                      # Not used with sqlite3.
            'PASSWORD': '123456789',                  # Not used with sqlite3.
            'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
        }
    }
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = "TuanTuan/static/img/upload/"#os.path.join(os.path.dirname(__file__),'static/img/upload/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/static/img/upload/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/TuanTuan/TuanTuanApp/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'
#ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__),'static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'hgvdka@s_9me@t^0*ivq!#$ni!rv5=cdnudlfd#0s13d7732!7'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'TuanTuan.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'TuanTuan.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'TuanTuanApp/templates'),
)

INSTALLED_APPS = (
	'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'grappelli',
    'TuanTuan.admin_bootstrap',
    'django.contrib.admin',
    'TuanTuan',
    'TuanTuan.TuanTuanApp',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
#import MySQLdb
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

#STATIC_ROOT = os.path.join(BASE_DIR, 'static').replace('\\', '/')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'TuanTuanApp/static').replace('\\', '/'),
    os.path.join(BASE_DIR, 'admin_bootstrap/static').replace('\\', '/'),
    os.path.join(BASE_DIR, 'static').replace('\\','/'),
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'TuanTuanApp/templates').replace('\\', '/'),
    os.path.join(BASE_DIR, 'admin_bootstrap/templates').replace('\\', '/'),
    os.path.join(BASE_DIR,  'ckeditor/templates/').replace('\\', '/'),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar':[
            ['Source','-','Save','Preview'],
            ['Cut','Copy','Paste','PasteText','PasteFromWord','-','SpellChecker'],
            ['Undo','Redo','-','Find','Replace','-','SelectAll','RemoveFormat'],
            ['Form','Checkbox','Radio','TextField','Textarea','Select','Button', 'ImageButton','HiddenField'],
            ['Styles','Format','Font','FontSize'],
            ['TextColor','BGColor'],
            ['Bold','Italic','Underline','Strike','-','Subscript','Superscript'],
            ['Link','Unlink','Anchor'],
            ['NumberedList','BulletedList','-','Outdent','Indent','Blockquote'],
            ['Image','Flash','Table','HorizontalRule','Smiley','SpecialChar','PageBreak'],
            ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
            ['Maximize','ShowBlocks','-','About']
        ],
        'width': 750,
        'height': 300,
        'toolbarCanCollapse': False,
        }
}

CKEDITOR_MEDIA_PREFIX = "/static/ckeditor/"
CKEDITOR_UPLOAD_PATH = ""
CKEDITOR_UPLOAD_PREFIX = "/static/img/upload/"
CKEDITOR_RESTRICT_BY_USER=True


