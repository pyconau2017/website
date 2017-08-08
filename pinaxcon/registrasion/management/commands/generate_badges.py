'''
Generate Conference Badges
==========================

Nearly all of the code in this was written by Richard Jones for the 2016 conference.
That code relied on the user supplying the attendee data in a CSV file, which Richard's
code then processed.

The main (and perhaps only real) difference, here, is that the attendee data are taken
directly from the database.  No CSV file is required.  (I may decide to add the ability
to process from a CSV, alternatively, later.  For now ... computer says no.)

Richard Jones <r1chardj0n3s@gmail.com>
Nick Seidenman <nick@seidenman.net>

PyCon AU 2017 Melbourne Team
'''
import sys
import os
import csv
from lxml import etree
import tempfile
from copy import deepcopy
import subprocess
#import progressbar

from django.conf import settings

from django.core.management.base import BaseCommand

from registrasion.contrib import badger

class Command(BaseCommand):
    help = """\
    Generate SVGs to print badges.

    Supply the template (--template=___) and the target directory for the output
    (--out-dir=___) on the command line.  With no other arguments on the command
    this will produce badges for all attendees found in the conference database.

    Specifying attendee usernames or email address on the command line will limit
    the badges printed to just those attendees matching.

    """

    def add_arguments(self, parser):
        parser.add_argument('--statsonly', help='Just generate badge stats',
                            action='store_true', default=False)
        parser.add_argument('--template', help='SVG template for creating badges',
                            default=os.path.join("pinaxcon/templates", settings.BADGER_DEFAULT_SVG_2PP))
        parser.add_argument('--out-dir', help='Directory where SVG files will be created.',
                            default="/tmp/badges")
        parser.add_argument('usernames', nargs='*', type=str)

    def handle(self, *args, **options):

        if options['statsonly']:
            badger.generate_stats(options)
        else:
            badger.generate_badges(options)
