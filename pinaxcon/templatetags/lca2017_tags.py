import cms_pages
import hashlib
import urllib

from decimal import Decimal
from django import template
from django.conf import settings
from django.contrib.staticfiles.templatetags import staticfiles
from easy_thumbnails.files import get_thumbnailer
from symposion.conference import models as conference_models
from symposion.schedule.models import Track

CONFERENCE_ID = settings.CONFERENCE_ID

register = template.Library()


@register.assignment_tag()
def classname(ob):
    return ob.__class__.__name__


@register.simple_tag(takes_context=True)
def can_manage(context, proposal):
    return proposal_permission(context, "manage", proposal)


@register.simple_tag(takes_context=True)
def can_review(context, proposal):
    return proposal_permission(context, "review", proposal)


def proposal_permission(context, permname, proposal):
    slug = proposal.kind.section.slug
    perm = "reviews.can_%s_%s" % (permname, slug)
    return context.request.user.has_perm(perm)


# {% load statictags %}{% static 'pyconau2017/images/svgs/illustrations/' %}{{ illustration }}

@register.simple_tag(takes_context=False)
def illustration(name):
    return staticfiles.static('pyconau2017/images/svgs/illustrations/') + name


@register.simple_tag(takes_context=True)
def speaker_photo(context, speaker, size):
    ''' Provides the speaker profile, or else fall back to libravatar or gravatar. '''

    if speaker.photo:
        thumbnailer = get_thumbnailer(speaker.photo)
        thumbnail_options = {'crop': True, 'size': (size, size)}
        thumbnail = thumbnailer.get_thumbnail(thumbnail_options)
        return thumbnail.url
    else:
        email = speaker.user.email.encode("utf-8")
        md5sum = hashlib.md5(email.strip().lower()).hexdigest()
        url = "https://secure.gravatar.com/avatar/%s?s=%d&d=%s" % (md5sum, size, "https://linux.conf.au/site_media/static/lca2017/images/speaker-fallback-devil.jpg")

        return url


@register.simple_tag()
def define(value):
    return value


@register.simple_tag()
def presentation_bg_number(presentation, count):
    return sum(ord(i) for i in presentation.title) % count


@register.simple_tag()
def header_paragraph(name):
    model = cms_pages.models.NamedHeaderParagraph
    try:
        return model.objects.get(name=name).text
    except model.DoesNotExist:
        return ""


@register.simple_tag()
def all_images():
    return cms_pages.models.CustomImage.objects.all().order_by("title")


@register.filter()
def gst(amount):
    two_places = Decimal(10) ** -2
    return Decimal(amount / 11).quantize(two_places)


@register.simple_tag()
def conference_name():
    return conference_models.Conference.objects.get(id=CONFERENCE_ID).title

@register.filter()
def trackname(room, day):
    try:
        track_name = room.track_set.get(day=day).name
    except Track.DoesNotExist:
        track_name = None
    return track_name
