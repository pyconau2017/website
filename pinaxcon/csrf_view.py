from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.template import Context, RequestContext, loader
from django.utils.translation import ugettext as _
from django.utils.version import get_docs_version

def csrf_failure(request, reason=""):

    from django.middleware.csrf import REASON_BAD_TOKEN, REASON_NO_REFERER, REASON_NO_CSRF_COOKIE
    t = loader.get_template("403_csrf.html")
    c = Context({
        'title': _("Forbidden"),
        'main': _("CSRF verification failed. Request aborted."),
        'reason': reason,
        'bad_token': reason == REASON_BAD_TOKEN,
        'no_referer': reason == REASON_NO_REFERER,
        'no_referer1': _(
            "You are seeing this message because this HTTPS site requires a "
            "'Referer header' to be sent by your Web browser, but none was "
            "sent. This header is required for security reasons, to ensure "
            "that your browser is not being hijacked by third parties."),
        'no_referer2': _(
            "If you have configured your browser to disable 'Referer' headers, "
            "please re-enable them, at least for this site, or for HTTPS "
            "connections, or for 'same-origin' requests."),
        'no_cookie': reason == REASON_NO_CSRF_COOKIE,
        'no_cookie1': _(
            "You are seeing this message because this site requires a CSRF "
            "cookie when submitting forms. This cookie is required for "
            "security reasons, to ensure that your browser is not being "
            "hijacked by third parties."),
        'no_cookie2': _(
            "If you have configured your browser to disable cookies, please "
            "re-enable them, at least for this site, or for 'same-origin' "
            "requests."),
        'DEBUG': settings.DEBUG,
        'docs_version': get_docs_version(),
        'more': _("More information is available with DEBUG=True."),
    })
    c = RequestContext(request, c)
    return HttpResponseForbidden(t.render(c), content_type='text/html')
