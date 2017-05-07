# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-05-07 06:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinaxcon_registrasion', '0004_auto_20160923_0133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendeeprofile',
            name='lca_chat',
        ),
        migrations.AlterField(
            model_name='attendeeprofile',
            name='lca_announce',
            field=models.BooleanField(help_text=b'Select to be subscribed to the low-traffic lca-announce mailing list', verbose_name=b'Subscribe to PyCon Announce'),
        ),
        migrations.AlterField(
            model_name='attendeeprofile',
            name='past_lca',
            field=models.ManyToManyField(blank=True, to='pinaxcon_registrasion.PastEvent', verbose_name=b'Which past PyCon Australia events have you attended?'),
        ),
    ]
