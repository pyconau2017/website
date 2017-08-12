'''
Update the `video_url` attribute of the *Presentation* model instances.

The A/V guys (Ryan Verner and co.) did and absolutely BRILLIANT job
of producing videos from the conference talks and tutes and getting
them up on youtube in record time.   They supply the website team with
a CSV file that includes the Presentation URLs and the YouTube URLs.
This management command takes that file and updates the database
so that talks that have videos on YouTube will have a [video] hyperlink
in their entry in the schedule table, making it easy to go to the
video directly from this table.

Note that if ``--empty--only`` is used, the number of instances updated
may or may not vary depending on how many actually had empty (or blank)
``video_url`` properties before the update.

Nick Seidenman (N6) <n6151h@gmail.com>
PyCon AU Melbourne 2017
Website Team
'''

import sys
import os
import csv
from lxml import etree
import tempfile
from copy import deepcopy
import subprocess
import progressbar

from django.conf import settings

from django.core.management.base import BaseCommand

from symposion.utils.videos import VideoURLUpdater

class Command(BaseCommand):
    help = """\
    Update the video_url property in the Presentation instances found
    in the CSV file supplied on the command line.
    """

    def add_arguments(self, parser):
        parser.add_argument('--empty-only', action='store_true', default=False,
                            help='Only update Presentations with blank video_url property.')
        parser.add_argument('av_updates', nargs='*', type=str)

    def handle(self, *args, **options):

        vu = VideoURLUpdater(options['av_updates'][0])
        vu.update(empty_only=options['empty_only'])
        print("{} presentations updated".format(len(vu)))