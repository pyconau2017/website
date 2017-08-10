import os
import logging

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pyconau_uat',
        'USER': 'pyconau_uat',
        'PASSWORD': 'sentByJoe',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

SECRET_KEY = "shhhh-it's-a-secret!"

DEBUG = True  # Set this to False for production systems.

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        # 'null': {
        #     'level':'DEBUG',
        #     'class':'django.utils.log.NullHandler',
        # },
         'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        # I always add this handler to facilitate separating loggings
         'log_file':{
             'level': 'DEBUG',
             'class': 'logging.handlers.RotatingFileHandler',
             'filename': os.path.join('/some/path/to/log/directory/pycon2017', 'log/django.log'),
             'maxBytes': 16777216, # 16megabytes
             'formatter': 'verbose'
         },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'symposion.request': {
            'handlers': ['mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'apps': { # I keep all my of apps under 'apps' folder, but you can also add them one by one, and this depends on how your virtualenv/paths are set
            'handlers': ['log_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    # you can also shortcut 'loggers' and just configure logging for EVERYTHING at once
    'root': {
        'handlers': ['console', 'log_file'], #'mail_admins'],
        'level': 'DEBUG'
    },
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"