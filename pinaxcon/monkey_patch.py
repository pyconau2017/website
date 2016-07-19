from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from functools import wraps


class MonkeyPatchMiddleware(object):
    ''' Ensures that our monkey patching only gets called after it is safe to do so.'''

    def process_request(self, request):
        do_monkey_patch()


def do_monkey_patch():
    patch_speaker_profile_form()
    patch_accounts_to_send_bcc()
    fix_sitetree_check_access_500s()
    never_cache_login_page()

    # Remove this function from existence
    global do_monkey_patch
    do_monkey_patch = lambda: None


def patch_speaker_profile_form():
    ''' Replaces textarea widgets with markdown editors. '''

    import widgets
    from symposion.speakers.forms import SpeakerForm

    fields = SpeakerForm.base_fields
    fields["biography"].widget = widgets.AceMarkdownEditor()
    fields["experience"].widget = widgets.AceMarkdownEditor()
    fields["accessibility"].widget = widgets.AceMarkdownEditor()


def patch_accounts_to_send_bcc():
    ''' Patches django-user-accounts' email functions to send a BCC e-mail to
    the default BCC e-mail address. '''

    from account import hooks

    # django-user-accounts always uses send_mail like:
    # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to)

    if hasattr(settings, "ENVELOPE_BCC_LIST"):
        bcc_email = settings.ENVELOPE_BCC_LIST
    else:
        bcc_email = None

    def send_mail(subject, message, from_email, to):
        email = EmailMultiAlternatives(
            subject,
            message,
            from_email,
            to,
            bcc=bcc_email,
        )
        email.send()

    hooks.send_mail = send_mail


def fix_sitetree_check_access_500s():
    ''' django-sitetree has a bug: https://github.com/idlesign/django-sitetree/pull/167/files
    -- it swallows the cause of all 500 errors. This swallows KeyErrors from
    the failing function. '''

    from sitetree.sitetreeapp import SiteTree

    old_check_access = SiteTree.check_access

    @wraps(SiteTree.check_access)
    def check_access(self, *a, **k):
        try:
            return old_check_access(self, *a, **k)
        except KeyError:
            return False

    SiteTree.check_access = check_access

def never_cache_login_page():
    from django.views.decorators.cache import never_cache
    from account.views import LoginView
    LoginView.get = never_cache(LoginView.get)
