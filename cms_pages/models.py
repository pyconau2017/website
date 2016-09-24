from __future__ import unicode_literals

from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.forms.utils import ErrorList
from django.http import Http404
from django.shortcuts import render
from django.utils.encoding import python_2_unicode_compatible

from modelcluster.fields import ParentalKey

from wagtail.wagtailadmin.edit_handlers import InlinePanel
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailadmin.edit_handlers import PageChooserPanel
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.url_routing import RouteResult

from wagtail.wagtailimages import blocks as imageblocks
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import AbstractImage
from wagtail.wagtailimages.models import AbstractRendition
from wagtail.wagtailimages.models import Image

from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet


from symposion import schedule

ILLUSTRATION_ANTARCTICA = "antarctica.svg"
ILLUSTRATION_BRIDGE = "bridge.svg"
ILLUSTRATION_CASINO = "casino.svg"
ILLUSTRATION_CRADLE = "cradle.svg"
ILLUSTRATION_DEVIL = "devil.svg"
ILLUSTRATION_FALLS = "falls.svg"
ILLUSTRATION_HOBART = "hobart.svg"
ILLUSTRATION_LAVENDER = "lavender.svg"
ILLUSTRATION_TUZ = "tuz.svg"
ILLUSTRATION_WINEGLASS = "wineglass.svg"

ILLUSTRATION_TYPES = (
    (ILLUSTRATION_ANTARCTICA, "Antarctica"),
    (ILLUSTRATION_BRIDGE, "Bridge"),
    (ILLUSTRATION_CASINO, "Casino"),
    (ILLUSTRATION_CRADLE, "Cradle Mountain"),
    (ILLUSTRATION_DEVIL, "Tasmanian Devil"),
    (ILLUSTRATION_FALLS, "Waterfall"),
    (ILLUSTRATION_HOBART, "Hobart"),
    (ILLUSTRATION_LAVENDER, "Lavender"),
    (ILLUSTRATION_TUZ, "Tuz"),
    (ILLUSTRATION_WINEGLASS, "Wineglass"),
)


class ExternalLinksBlock(blocks.StructBlock):

    class Meta:
        template = "cms_pages/home_page_blocks/external_link.html"

    EXTERNAL_LINK_TWITTER = "twitter"
    EXTERNAL_LINK_FACEBOOK = "facebook"
    EXTERNAL_LINK_GENERIC = "generic"

    EXTERNAL_LINK_TYPES = (
        (EXTERNAL_LINK_TWITTER, "Twitter"),
        (EXTERNAL_LINK_FACEBOOK, "Facebook"),
        (EXTERNAL_LINK_GENERIC, "Generic URL"),
    )

    alt = blocks.CharBlock(required=True)
    icon = blocks.ChoiceBlock(
        choices=EXTERNAL_LINK_TYPES,
        required=True,
    )
    url = blocks.URLBlock(required=True)


class BasicContentLink(blocks.StructBlock):

    page = blocks.PageChooserBlock(
        required=False,
        help_text="You must specify either this, or the URL.",
    )
    url = blocks.CharBlock(
        required=False,
        help_text="You must specify either this, or the URL.",
    )
    title = blocks.CharBlock(required=True)


class BasicContentBlock(blocks.StructBlock):

    class Meta:
        template = "cms_pages/home_page_blocks/basic_content.html"

    PANEL_BLUE_LEFT = "blue_left"
    PANEL_WHITE_RIGHT = "white_right"
    PANEL_TYPES = (
        (PANEL_BLUE_LEFT, "Left-aligned image, blue-filtered image BG"),
        (PANEL_WHITE_RIGHT, "Right-aligned image, white background"),
    )

    panel_type = blocks.ChoiceBlock(
        choices=PANEL_TYPES,
        required=True,
    )
    heading = blocks.CharBlock(required=True)
    inset_illustration = blocks.ChoiceBlock(
        choices=ILLUSTRATION_TYPES,
        required=True,
    )
    background_image = imageblocks.ImageChooserBlock(
        required=False,
        help_text="This is used as the background image of a "
                  "blue-left block. It's not used for white-right."
    )
    body = blocks.RichTextBlock(required=True)
    link = BasicContentLink()
    external_links = blocks.ListBlock(ExternalLinksBlock)
    compact = blocks.BooleanBlock(
        required=False,
        help_text="True if this block is to be displayed in 'compact' mode",
    )


class PresentationChooserBlock(blocks.ChooserBlock):
    target_model = schedule.models.Presentation
    widget = forms.Select

    # Return the key value for the select field
    def value_for_form(self, value):
        if isinstance(value, self.target_model):
            return value.pk
        else:
            return value


class KeynoteSpeakerBlock(blocks.StructBlock):

    class Meta:
        template = "cms_pages/home_page_blocks/keynote_speaker.html"

    name = blocks.CharBlock(required=True)
    body = blocks.RichTextBlock(required=True)
    links = blocks.ListBlock(ExternalLinksBlock)
    profile_image = imageblocks.ImageChooserBlock(
        required=False,
        help_text="Profile image for the speaker",
    )
    presentation = PresentationChooserBlock(
        help_text="This speaker's presentation",
    )


class KeynotesBlock(blocks.StructBlock):

    class Meta:
        template = "cms_pages/home_page_blocks/keynotes.html"

    heading = blocks.CharBlock(required=True)
    speakers = blocks.ListBlock(KeynoteSpeakerBlock)


class HomePage(Page):

    body = StreamField([
        ("basic_content", BasicContentBlock()),
        ("keynotes", KeynotesBlock()),
        # TODO: other bits
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]


# Content pages

class FloatingImageBlock(imageblocks.ImageChooserBlock):

    class Meta:
        template = "cms_pages/content_page_blocks/floating_image.html"


class AnchorBlock(blocks.CharBlock):

    class Meta:
        template = "cms_pages/content_page_blocks/anchor.html"


class ColophonImageListBlock(blocks.StructBlock):

    class Meta:
        template = "cms_pages/content_page_blocks/colophon.html"

    do_nothing = blocks.BooleanBlock(required=False)


class AbstractContentPage(Page):

    class Meta:
        abstract = True

    intro = models.CharField(max_length=250)

    body = StreamField([
        ("rich_text", blocks.RichTextBlock(required=False)),
        ("raw_html", blocks.RawHTMLBlock(required=False)),
        ("floating_image", FloatingImageBlock()),
        ("anchor", AnchorBlock(
            help_text="Add a named anchor to this point in the page"
        )),
        ("colophon_image_list", ColophonImageListBlock()),
    ])

    background_image = models.ForeignKey(
        'CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        ImageChooserPanel('background_image'),
        FieldPanel('intro'),
        StreamFieldPanel('body')
    ]


class ContentPage(AbstractContentPage):

    inset_illustration = models.CharField(
        choices=ILLUSTRATION_TYPES,
        max_length=256,
    )

    content_panels = AbstractContentPage.content_panels + [
        FieldPanel('inset_illustration')
    ]


# News pages

class NewsIndexPage(AbstractContentPage):

    def route(self, request, path_components):

        # Try the default to allow children to resolve
        try:
            return super(NewsIndexPage, self).route(request, path_components)
        except Http404:
            pass

        if path_components:
            # tell Wagtail to call self.serve() with an additional 'path_components' kwarg
            return RouteResult(self, kwargs={'path_components': path_components})
        else:
            raise Http404

    def serve(self, request, path_components=[]):
        ''' Optionally return the RSS version of the page '''

        template = self.template

        if path_components and path_components[0] == "rss":
            template = template.replace(".html", ".rss")

        r = super(NewsIndexPage, self).serve(request)
        r.template_name = template
        return r

    def child_pages(self):
        return NewsPage.objects.live().child_of(self).specific().order_by("-date")

    subpage_types = [
        "NewsPage",
    ]

    content_panels = AbstractContentPage.content_panels


class NewsPage(AbstractContentPage):

    date = models.DateField("Post date")

    portrait_image = models.ForeignKey(
        'CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    parent_page_types = [
        NewsIndexPage,
    ]

    content_panels = AbstractContentPage.content_panels + [
        FieldPanel('date'),
        ImageChooserPanel('portrait_image'),
    ]


@register_snippet
@python_2_unicode_compatible
class ScheduleHeaderParagraph(models.Model):
    ''' Used to show the paragraph in the header for a schedule page. '''
    schedule = models.OneToOneField(
        schedule.models.Schedule,
        related_name="header_paragraph",
    )
    text = models.TextField()

    panels = [
        FieldPanel('schedule'),
        FieldPanel('text'),
    ]

    def __str__(self):
        return str(self.schedule)


@register_snippet
@python_2_unicode_compatible
class NamedHeaderParagraph(models.Model):
    ''' Used to show the paragraph in the header for a schedule page. '''
    name = models.CharField(
        max_length=64,
        help_text="Pass this name to header_paragraph tag.",
    )
    text = models.TextField()

    panels = [
        FieldPanel('name'),
        FieldPanel('text'),
    ]

    def __str__(self):
        return str(self.name)


# Image models -- copied from wagtail docs


class CustomImage(AbstractImage):
    # Add any extra fields to image here

    # eg. To add a caption field:
    copyright_year = models.CharField(
        max_length=64,
        help_text="The year the image was taken",
    )
    licence = models.CharField(
        max_length=64,
        help_text="The short-form code for the licence (e.g. CC-BY)",
    )
    author = models.CharField(
        max_length=255,
        help_text="The name of the author of the work",
    )
    source_url = models.URLField(
        help_text="The URL where you can find the original of this image",
    )

    admin_form_fields = Image.admin_form_fields + (
        "copyright_year",
        "licence",
        "author",
        "source_url",
    )


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(CustomImage, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter', 'focal_point_key'),
        )


# Delete the source image file when an image is deleted
@receiver(pre_delete, sender=CustomImage)
def image_delete(sender, instance, **kwargs):
    instance.file.delete(False)


# Delete the rendition image file when a rendition is deleted
@receiver(pre_delete, sender=CustomRendition)
def rendition_delete(sender, instance, **kwargs):
    instance.file.delete(False)
