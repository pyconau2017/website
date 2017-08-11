import os
import dj_database_url

import bleach

# Just going to put this comment in here to make a change that I'll back out later.

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = PACKAGE_ROOT

# Change this in local_settings.py
SITE_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

LOGIN_URL = '/account/login/'

# Change/set this in local_settings.py
DEBUG = False

# Set this in local_settings.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(PROJECT_ROOT, "dev.db"),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Set this in local_settings.py
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', ]

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
    "debug_toolbar.middleware.DebugToolbarMiddleware",
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
    "debug_toolbar",

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
    "markdownify",

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
    "nested_admin",

    # Registrasion-stipe
    "pinax.stripe",
    "django_countries",
    "registripe",

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

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': lambda x: DEBUG,
}

# LOGGING configuratoin can be found in local_settings.py
# Using django default logging config otherwise.

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

# NOTE: Only use console.EmailBackend for debugging.
#EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25

DEFAULT_FROM_EMAIL = "contact@pycon-au.org"
ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True
ACCOUNT_LOGIN_REDIRECT_URL = "dashboard"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2
ACCOUNT_USE_AUTH_AUTHENTICATE = True

THEME_CONTACT_EMAIL = "contact@pycon-au.org"

AUTHENTICATION_BACKENDS = [
    "symposion.teams.backends.TeamPermissionsBackend",
    "account.auth_backends.UsernameAuthenticationBackend",
    "account.auth_backends.EmailAuthenticationBackend",
]

CONFERENCE_ID = 1
PROPOSAL_FORMS = {
    "talk": "pinaxcon.proposals.forms.TalkProposalForm",
    "pyconautalk": "pinaxcon.proposals.forms.PyConAuProposalForm",
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
TICKET_PRODUCT_CATEGORY = 1

# Wagtail config
WAGTAIL_SITE_NAME = 'Pycon Australia 2017'
WAGTAIL_APPEND_SLASH = True
WAGTAILIMAGES_IMAGE_MODEL = 'cms_pages.CustomImage'

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

BLEACH_ALLOWED_TAGS = bleach.ALLOWED_TAGS + ['p']

# Badge Generation -- Badger
BADGER_DEFAULT_SVG = "registrasion/badge.svg"         # One badge per page.
BADGER_DEFAULT_SVG_2PP = "registrasion/badge-2pp.svg"    # Two badges on single page.
BADGER_DEFAULT_FORM = "registrasion/badge_form.html"

# Production settings have their own file to override stuff here
try:
    LOCAL_SETTINGS
except NameError:
    try:
        from local_settings import *
    except ImportError:
        pass

