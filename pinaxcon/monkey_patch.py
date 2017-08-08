from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from functools import wraps


class MonkeyPatchMiddleware(object):
    ''' Ensures that our monkey patching only gets called after it is safe to do so.'''

    def process_request(self, request):
        do_monkey_patch()


def do_monkey_patch():
    patch_speaker_profile_form()
    patch_mail_to_send_bcc()
    fix_sitetree_check_access_500s()
    never_cache_login_page()
    patch_stripe_payment_form()

    # Remove this function from existence
    global do_monkey_patch
    do_monkey_patch = lambda: None


def patch_speaker_profile_form():
    ''' Replaces textarea widgets with markdown editors. '''

    from . import widgets
    from symposion.speakers.forms import SpeakerForm

    fields = SpeakerForm.base_fields
    fields["biography"].widget = widgets.AceMarkdownEditor()
    fields["experience"].widget = widgets.AceMarkdownEditor()
    fields["accessibility"].widget = widgets.AceMarkdownEditor()


def patch_mail_to_send_bcc():
    ''' Patches django.core.mail's message classes to send a BCC e-mail to
    the default BCC e-mail address. '''

    from django.core.mail import message

    ARG = "bcc"

    if hasattr(settings, "ENVELOPE_BCC_LIST"):
        bcc_email = settings.ENVELOPE_BCC_LIST
    else:
        return  # We don't need to do this patch.

    def bcc_arg_position(f):
        ''' Returns the position of 'bcc' in the argument list to f, or None if
        there is no such argument. '''
        co = f.__code__
        # The first co_argcount members of co_varnames are argument variables
        for i, argname in enumerate(co.co_varnames[:co.co_argcount]):
            if argname == ARG:
                return i
        else:
            return None

    def bcc_is_provided_positionally(f, a):
        ''' Returns true if 'bcc' is provided as a positional argument to f,
        when it is called with the argument list `a`. '''

        return bcc_arg_position(f) < len(a)

    def patch_bcc_positional(f, a):
        ''' Returns a copy of `a`, but with the bcc argument patched to include
        our BCC list. '''

        pos = bcc_arg_position(f)
        bcc = a[pos]

        if bcc is not None:
            bcc = list(bcc)
        else:
            bcc = []

        bcc += bcc_email

        return tuple(a[:pos] + (bcc,) + a[pos + 1:])


    def patch_bcc_keyword(f, k):
        ''' Adds our BCC list to the BCC list in the keyword arguments, and
        returns the new version of the keyword arguments.

        Arguments:
            f (callable): The function that we're patching. It should have an
                argument called bcc.
            k (dict): A dictionary of kwargs to be provided to EmailMessage.
            It will be modified to add the BCC list specified in
            settings.ENVELOPE_BCC_LIST, if provided.
        '''

        if ARG in k:
            bcc = list(k[ARG])
            del k[ARG]
        else:
            bcc = []
        bcc += list(bcc_email)
        k[ARG] = bcc

        return k

    to_wrap = message.EmailMessage.__init__

    @wraps(to_wrap)
    def email_message__init__(*a, **k):

        if bcc_is_provided_positionally(to_wrap, a):
            a = patch_bcc_positional(to_wrap, a)
        else:
            k = patch_bcc_keyword(to_wrap, k)

        return to_wrap(*a, **k)

    message.EmailMessage.__init__ = email_message__init__

    # Do not need to wrap EmailMultiAlternatives because it is a subclass of
    # EmailMessage.


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


def patch_stripe_payment_form():

    import inspect  # Oh no.
    from django.http.request import HttpRequest
    from registripe.forms import CreditCardForm
    from pinaxcon.registrasion import models

    old_init = CreditCardForm.__init__

    @wraps(old_init)
    def new_init(self, *a, **k):

        # Map the names from our attendee profile model
        # To the values expected in the Stripe card model
        mappings = (
            ("address_line_1", "address_line1"),
            ("address_line_2", "address_line2"),
            ("address_suburb", "address_city"),
            ("address_postcode", "address_zip"),
            ("state", "address_state"),
            ("country", "address_country"),
        )

        initial = "initial"
        if initial not in k:
            k[initial] = {}
        initial = k[initial]

        # Find request context maybe?
        frame = inspect.currentframe()
        attendee_profile = None
        if frame:
            context = frame.f_back.f_locals
            for name, value in (context.items() or {}):
                if not isinstance(value, HttpRequest):
                    continue
                user = value.user
                if not user.is_authenticated():
                    break
                try:
                    attendee_profile = models.AttendeeProfile.objects.get(
                        attendee__user=user
                    )
                except models.AttendeeProfile.DoesNotExist:
                    # Profile is still none.
                    pass
                break

        if attendee_profile:
            for us, stripe in mappings:
                i = getattr(attendee_profile, us, None)
                if i:
                    initial[stripe] = i

        old_init(self, *a, **k)

    CreditCardForm.__init__ = new_init
