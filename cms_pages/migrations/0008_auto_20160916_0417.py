# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from wagtail.wagtailcore.rich_text import RichText


models = ["ContentPage", "NewsIndexPage", "NewsPage", ]


def convert_to_streamfield(apps, schema_editor):
    for model_name in models:
        _convert_to_streamfield(apps, model_name)


def _convert_to_streamfield(apps, model_name):
    Model = apps.get_model("cms_pages", model_name)
    for page in Model.objects.all():
        if page.body.raw_text and not page.body:
            page.body = [('rich_text', RichText(page.body.raw_text))]
            page.save()


def convert_to_richtext(apps, schema_editor):
    for model_name in models:
        _convert_to_richtext(apps, model_name)


def _convert_to_richtext(apps, model_name):
    Model = apps.get_model("cms_pages", model_name)
    for page in Model.objects.all():
        if page.body.raw_text is None:
            raw_text = ''.join([
                child.value.source for child in page.body
                if child.block_type == 'rich_text'
            ])
            page.body = raw_text
            page.save()


class Migration(migrations.Migration):

    dependencies = [
        ('cms_pages', '0007_auto_20160916_0417'),
    ]

    operations = [
        migrations.RunPython(
            convert_to_streamfield,
            convert_to_richtext,
        ),
    ]
