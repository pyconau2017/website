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

    Default columns within the CSV are 4 and 5.  These can be changed using
    the --pr-col and --yt-col switches.  The offset from the end of the
    presentation URL for the presentation's pk can be set using the --pkndx
    switch.  IT IS INADVISABLE TO CHANGE THESE UNLESS YOU KNOW WHAT YOU ARE
    DOING!  YOU HAVE BEEN WARNED!
    """

    def add_arguments(self, parser):
        parser.add_argument('--empty-only', action='store_true', default=False,
                            help='Only update Presentations with blank video_url property.')
        parser.add_argument('--pr-col', type=int, default=4,
                            help='Column (from 0) of presentation URL. [4]')
        parser.add_argument('--yt-col', type=int, default=5,
                            help='Column (fron 0) of youtube URL. [5]')
        parser.add_argument('--pkndx', type=int, default=2,
                            help='Column (fron 0) of youtube URL. [5]')
        parser.add_argument('av_updates', nargs='*', type=str)

    def handle(self, *args, **options):

        vu = VideoURLUpdater(options['av_updates'][0],  pr_col=options['pr_col'],
                  yt_col=options['yt_col'], pkndx=options['pkndx'])
        vu.update(empty_only=options['empty_only'])
        print("{} presentations updated".format(len(vu)))