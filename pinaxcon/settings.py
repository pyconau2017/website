import os
import dj_database_url


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = PACKAGE_ROOT

DEBUG = False #bool(int(os.environ.get("DEBUG", "1")))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(PROJECT_ROOT, "dev.db"),
    },
    #'default': {
    #    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #    'NAME': 'pycon2017_prod',
    #    'USER': 'pycon2017_prod',
    #    'PASSWORD': 'udoo9YooEa0eutei',
    #    'HOST': '172.16.0.100',
    #    'PORT': '',
    #}
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}


ALLOWED_HOSTS = ['2017.pycon-au.org', 'zookeepr1.linux.org.au']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "Australia/Melbourne"

# The date format for this installation
DATE_FORMAT = "j F Y"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-au"

SITE_ID = int(os.environ.get("SITE_ID", 1))

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/site_media/media/"

# Absolute path to the directory static files should be collected to.
# Don"t put anything in this directory yourself; store your static files
# in apps" "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/site_media/static/"

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static", "dist"),
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Make this unique, and don't share it with anybody.
SECRET_KEY = "6r&z0i#!k-thu4nv^zzx!f$fbp(&#2i5mq_^%%@ihu_qxxotl_"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PACKAGE_ROOT, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.core.context_processors.debug",
                "django.core.context_processors.i18n",
                "django.core.context_processors.media",
                "django.core.context_processors.static",
                "django.core.context_processors.tz",
                "django.core.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "account.context_processors.account",
                "pinax_theme_bootstrap.context_processors.theme",
                "symposion.reviews.context_processors.reviews",
                "sekizai.context_processors.sekizai",
            ],
        },
    },
]

MIDDLEWARE_CLASSES = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "reversion.middleware.RevisionMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
    'pinaxcon.monkey_patch.MonkeyPatchMiddleware',
]

ROOT_URLCONF = "pinaxcon.urls"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "pinaxcon.wsgi.application"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.contrib.humanize",

    # theme
    "bootstrapform",
    "pinax_theme_bootstrap",

    # external
    "account",
    "easy_thumbnails",
    "taggit",
    "reversion",
    "metron",
    "sitetree",
    "pinax.eventlog",

    # wagtail
    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',

    'modelcluster',


    # symposion
    "symposion",
    "symposion.conference",
    "symposion.proposals",
    "symposion.reviews",
    "symposion.schedule",
    "symposion.speakers",
    "symposion.sponsorship",
    "symposion.teams",
    "pinax.boxes",

    # Registrasion
    "registrasion",

    # Registrasion-stipe
    "pinax.stripe",
    "django_countries",
    "registripe",

    #admin - required by registrasion ??
    "nested_admin",

    # project
    "cms_pages",
    "pinaxcon",
    "pinaxcon.proposals",
    "pinaxcon.registrasion",
    "jquery",
    "djangoformsetjs",

    # wiki
    "django_nyt",
    "mptt",
    "sekizai",
    "sorl.thumbnail",
    "wiki",
    "wiki.plugins.attachments",
    "wiki.plugins.notifications",
    "wiki.plugins.images",
    "wiki.plugins.macros",


    #testing
    "django_nose",
]


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
             'filename': os.path.join('/srv/http/2017.pycon-au.org', 'log/django.log'),
             'maxBytes': '16777216', # 16megabytes
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
        'apps': { # I keep all my of apps under 'apps' folder, but you can also add them one by one, and this depends on how your virtualenv/paths are set
            'handlers': ['log_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    # you can also shortcut 'loggers' and just configure logging for EVERYTHING at once
    'root': {
        'handlers': ['console', 'mail_admins'],
        'level': 'DEBUG'
    },
}
FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = False
ACCOUNT_LOGIN_REDIRECT_URL = "dashboard"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2
ACCOUNT_USE_AUTH_AUTHENTICATE = True

THEME_CONTACT_EMAIL = "pyconau-orgs@lists.linux.org.au"

AUTHENTICATION_BACKENDS = [
    "symposion.teams.backends.TeamPermissionsBackend",
    "account.auth_backends.UsernameAuthenticationBackend",
    "account.auth_backends.EmailAuthenticationBackend",
]

CONFERENCE_ID = 1
PROPOSAL_FORMS = {
    "talk": "pinaxcon.proposals.forms.TalkProposalForm",
    "tutorial": "pinaxcon.proposals.forms.TutorialProposalForm",
    "miniconf": "pinaxcon.proposals.forms.MiniconfProposalForm",
    "sysadmin-miniconf": "pinaxcon.proposals.forms.SysAdminProposalForm",
    "openradio-miniconf": "pinaxcon.proposals.forms.RadioProposalForm",
    "wootconf-miniconf": "pinaxcon.proposals.forms.WootconfProposalForm",
    "writethedocs-miniconf": "pinaxcon.proposals.forms.WriteTheDocsProposalForm",
    "security-miniconf": "pinaxcon.proposals.forms.SecurityProposalForm",
    "kernel-miniconf": "pinaxcon.proposals.forms.KernelProposalForm",
    "games-miniconf": "pinaxcon.proposals.forms.GamesProposalForm",
    "testing-miniconf": "pinaxcon.proposals.forms.TestingProposalForm",
    "knowledge-miniconf": "pinaxcon.proposals.forms.KnowledgeProposalForm",
    "lawpolicy-miniconf": "pinaxcon.proposals.forms.LawProposalForm",
    "openhardware-miniconf": "pinaxcon.proposals.forms.OpenHardwareProposalForm",
}

#PINAX_PAGES_HOOKSET = "pinaxcon.hooks.PinaxPagesHookSet"
#PINAX_BOXES_HOOKSET = "pinaxcon.hooks.PinaxBoxesHookSet"

# Registrasion bits:
ATTENDEE_PROFILE_MODEL = "pinaxcon.registrasion.models.AttendeeProfile"
ATTENDEE_PROFILE_FORM = "pinaxcon.registrasion.forms.ProfileForm"
INVOICE_CURRENCY = "AUD"
PINAX_STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", "your test public key")
PINAX_STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "your test secret key")
PINAX_STRIPE_SEND_EMAIL_RECEIPTS = False

# Wagtail config
WAGTAIL_SITE_NAME = 'Pycon Australia 2017'
WAGTAIL_APPEND_SLASH = True
WAGTAILIMAGES_IMAGE_MODEL = 'cms_pages.CustomImage'

ATTENDEE_PROFILE_FORM = "pinaxcon.registrasion.forms.ProfileForm"

# CSRF custom error screen
CSRF_FAILURE_VIEW = "pinaxcon.csrf_view.csrf_failure"

# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

ADMIN_USERNAMES = []

# Wiki settings
WIKI_CHECK_SLUG_URL_AVAILABLE = False

# Tell nose to measure coverage on the 'foo' and 'bar' apps
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=registrasion.controllers,registrasion.models',
]

WIKI_CAN_READ = True
WIKI_CAN_WRITE = True
WIKI_CAN_DELETE = True
WIKI_ACCOUNT_HANDLING = False

# Production settings have their own file to override stuff here
try:
    LOCAL_SETTINGS
except NameError:
    try:
        from local_settings import *
    except ImportError:
        pass
