from __future__ import unicode_literals

from django.http import Http404
from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore import blocks
from wagtail.wagtailimages import blocks as imageblocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.url_routing import RouteResult
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailadmin.edit_handlers import InlinePanel
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailadmin.edit_handlers import PageChooserPanel
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailsearch import index

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
    link = blocks.StructBlock([
        ("page", blocks.PageChooserBlock()),
        ("title", blocks.CharBlock(required=True)),
    ])
    external_links = blocks.ListBlock(ExternalLinksBlock)


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
    # TODO choice block that links to presentation page.


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
class AbstractContentPage(Page):

    class Meta:
        abstract = True

    intro = models.CharField(max_length=250)

    body = StreamField([
        ("rich_text", blocks.RichTextBlock(required=False)),
    ])

    background_image = models.ForeignKey(
        'wagtailimages.Image',
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
        'wagtailimages.Image',
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
