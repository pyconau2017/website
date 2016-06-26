from __future__ import unicode_literals

from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore import blocks
from wagtail.wagtailimages import blocks as imageblocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailadmin.edit_handlers import InlinePanel
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailadmin.edit_handlers import PageChooserPanel
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailsearch import index


class HomePage(Page):

    BASIC_CONTENT_BLUE_LEFT = 1
    BASIC_CONTENT_WHITE_RIGHT = 2
    BASIC_CONTENT_TYPES = (
        (BASIC_CONTENT_BLUE_LEFT, "Left-aligned image, blue-filtered image BG"),
        (BASIC_CONTENT_WHITE_RIGHT, "Right-aligned image, white background"),
    )

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

    EXTERNAL_LINK_TWITTER = "twitter.svg"
    EXTERNAL_LINK_FACEBOOK = "facebook.svg"
    EXTERNAL_LINK_LINKEDIN = "linkedin.svg"
    EXTERNAL_LINK_GENERIC = "generic.svg"

    EXTERNAL_LINK_TYPES = (
        (EXTERNAL_LINK_TWITTER, "Twitter"),
        (EXTERNAL_LINK_FACEBOOK, "Facebook"),
        (EXTERNAL_LINK_LINKEDIN, "LinkedIn"),
        (EXTERNAL_LINK_GENERIC, "Generic URL"),
    )

    body = StreamField([
        ("basic_content", blocks.StructBlock([
            ("type", blocks.ChoiceBlock(
                choices=BASIC_CONTENT_TYPES,
                required=True,
            )),
            ("heading", blocks.CharBlock(required=True)),
            ("inset_illustration", blocks.ChoiceBlock(
                choices=ILLUSTRATION_TYPES,
                required=True,
            )),
            ("background_image", imageblocks.ImageChooserBlock(
                required=False,
                help_text="This is used as the background image of a "
                          "blue-left block. It's not used for white-right."
            )),
            ("body", blocks.RichTextBlock(required=True)),
            ("link", blocks.StructBlock([
                ("page", blocks.PageChooserBlock()),
                ("title", blocks.CharBlock(required=True)),
            ])),
            ("external_links", blocks.ListBlock(
                blocks.StructBlock([
                    ("alt", blocks.CharBlock(required=True)),
                    ("icon", blocks.ChoiceBlock(
                        choices=EXTERNAL_LINK_TYPES,
                        required=True,
                    )),
                    ("url", blocks.URLBlock(required=True)
                )])
            )),
        ])),
        # TODO: keynotes
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
    body = RichTextField(blank=True)
    main_image = models.ForeignKey(
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
        ImageChooserPanel('main_image'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full")
    ]


class ContentPage(AbstractContentPage):

    IMAGE_DISPLAY_FEATURE = 1
    IMAGE_DISPLAY_VIGNETTE = 2

    IMAGE_DISPLAY = (
        (IMAGE_DISPLAY_FEATURE, "Banner with background feature image"),
        (IMAGE_DISPLAY_VIGNETTE, "No banner, circular vignette"),
    )

    image_display = models.IntegerField(
        choices=IMAGE_DISPLAY,
    )

    def image_display_feature(self):
        return self.image_display == IMAGE_DISPLAY_FEATURE

    def image_display_vignette(self):
        return self.image_display == IMAGE_DISPLAY_VIGNETTE

    content_panels = [
        FieldPanel('image_display')
    ] + AbstractContentPage.content_panels


# News pages

class NewsIndexPage(Page):
    intro = RichTextField(blank=True)

    subpage_types = [
        "NewsPage",
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
    ]


class NewsPage(AbstractContentPage):
    date = models.DateField("Post date")

    parent_page_types = [
        NewsIndexPage,
    ]

    content_panels = AbstractContentPage.content_panels + [
        FieldPanel('date'),
    ]
