'''
Generate Conference Badges
==========================

Nearly all of the code in this was written by Richard Jones for the 2016 conference.
That code relied on the user supplying the attendee data in a CSV file, which Richard's
code then processed.

The main (and perhaps only real) difference, here, is that the attendee data are taken
directly from the database.  No CSV file is required.  (I may decide to add the ability
to process from a CSV, alternatively, later.  For now ... computer says no.)

'''
import sys
import os
import csv
from lxml import etree
from copy import deepcopy
import subprocess
import progressbar

import pdb

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pinaxcon.registrasion.models import AttendeeProfile
from registrasion.controllers.cart import CartController
from registrasion.controllers.invoice import InvoiceController
from registrasion.models import Voucher
from registrasion.models import Attendee
from registrasion.models import Product
from registrasion.models import Invoice
from symposion.speakers.models import Speaker

# A few unicode encodings ...
GLYPH_PLUS = '+'
GLYPH_GLASS = u'\ue001'
GLYPH_DINNER = u'\ue179'
GLYPH_SPEAKER = u'\ue122'
GLYPH_SPRINTS = u'\ue254'
GLYPH_CROWN = u'\ue211'
GLYPH_SNOWMAN = u'\u2603'
GLYPH_STAR = u'\ue007'
GLYPH_FLASH = u'\ue162'

# Some company names are too long to fit on the badge, so, we
# define abbreviations here.
overrides = {
 "Optiver Pty. Ltd.": "Optiver",
 "IRESS Market Tech": "IRESS",
 "The Bureau of Meteorology": "BoM",
 "Google Australia": "Google",
 "Facebook Inc.": "Facebook",
 "Rhapsody Solutions Pty Ltd": "Rhapsody Solutions",
 "PivotNine Pty Ltd": "PivotNine",
 "SEEK Ltd.": "SEEK",
 "UNSW Australia": "UNSW",
 "Dev Demand Co": "Dev Demand",
 "Cascode Labs Pty Ltd": "Cascode Labs",
 "CyberHound Pty Ltd": "CyberHound",
 "Self employed Contractor": "",
 "Data Processors Pty Lmt": "Data Processors",
 "Bureau of Meterology": "BoM",
 "Google Australia Pty Ltd": "Google",
 # "NSW Rural Doctors Network": "",
 "Sense of Security Pty Ltd": "Sense of Security",
 # "Capital Numbers Australia": "",
 # "Monash University Student": "",
 # "General Dynamics Mediaware": "",
 # "Marklar Marklar Consulting": "",
 # "John Monash Science School": "",
 # "the Interaction Consortium": "",
 # "General Dynamics Mediaware": "",
 "Hewlett Packard Enterprose": "HPE",
 "Hewlett Packard Enterprise": "HPE",
 "CISCO SYSTEMS INDIA PVT LTD": "CISCO",
 "The University of Melbourne": "University of Melbourne",
 # "Console Technology Australia": "",
 # "The Information Access Group": "",
 # "University of South Carolina": "",
 # "APN Australian Regional Media": "",
 "Peter MacCallum Cancer Centre": "Peter Mac",
 "Commonwealth Bank of Australia": "CBA",
 "VLSCI, University of Melbourne": "VLSCI",
 "Australian Bureau of Meteorology": "BoM",
 "Bureau of Meteorology": "BoM",
 "Bureau of Meteorology, Australia": "BoM",
 "QUT Digital Media Research Centre": "QUT",
 "Dyn - Dynamic Network Services Inc": "Dyn",
 # "Office of Environment and Heritage": "",
 "The Australian National University": "ANU",
 # "Victoria Clinical Genetic Services": "",
 # "St. Joseph's College Gregory Terrace": "",
 "Murdoch Childrens Research Institute": "MCRI",
 "Centenary Institute, University of Sydney": "Centenary Institute",
 "Synchrotron Light Source Australia Pty Ltd": "Australian Synchrotron",
 "Australian Communication and Media Authority": "ACMA",
 "Dept. of Education - Camden Haven High School": "Camden Haven High School",
 "Australian Government - Bureau of Meteorology": "BoM",
 "The Walter and Eliza Hall Institute of Medical Research": "WEHI",
 "Dept. Parliamentary Services, Australian Parliamentary Library": "Dept. Parliamentary Services",
}


def text_size(text, prev=9999):
    '''
    Calculate the length of a text string as it relates to font size.
    '''
    n = len(text)
    size = int(min(70, max(25, 25 + 45 * (1 - (n - 7) / 17.))))
    return min(prev, size)


def set_text(soup, text_id, text, resize=None):
    '''
    Set the text value of an element (via beautiful soup calls).
    '''
    elem = soup.find(".//*[@id='%s']/{http://www.w3.org/2000/svg}tspan" % text_id)
    if elem is None:
        raise ValueError('could not find tag id=%s' % text_id)
    elem.text = text
    if resize:
        style = elem.get('style')
        elem.set('style', style.replace('font-size:70px', 'font-size:%dpx' % resize))


def set_colour(soup, slice_id, colour):
    '''
    Set colour of an element (using beautiful soup calls).
    '''
    elem = soup.find(".//*[@id='%s']" % slice_id)
    if elem is None:
        raise ValueError('could not find tag id=%s' % slice_id)
    style = elem.get('style')
    elem.set('style', style.replace('fill:#316a9a', 'fill:#%s' % colour))

def generate_badge(soup, data, n):
    '''
    Do the actual "heavy lifting" to create the badge SVG
    '''
    side = 'lr'[n]
    for tb in 'tb':
        part = tb + side
        size = text_size(data['firstname'])
        set_text(soup, 'firstname-' + part, data['firstname'], size)
        size = text_size(data['lastname'], size)
        set_text(soup, 'lastname-' + part, data['lastname'], size)
        size = text_size(data['company'], size * .8)

        name = data['firstname'] + data['lastname']

        # Richard, why is THIS here????
        if name == 'AshleyRead':
            data['ticket'] = 'Enthusiast'

        # Organiser/Team > Speaker/Volunteer > Contributor > Professional > Enthusiast > Student
        if 'Organiser' in data['ticket']:
            set_text(soup, 'ticket-' + part, 'Organiser')
            set_text(soup, 'company-' + part, data['company'], size)
        elif 'Volunteer' in data['ticket']:
            set_text(soup, 'ticket-' + part, 'Volunteer')
            set_text(soup, 'company-' + part, data['company'], size)
        elif 'Speaker' in data['ticket']:
            set_text(soup, 'ticket-' + part, 'Speaker')
            set_text(soup, 'company-' + part, data['company'], size)
        elif 'Contributor' in data['ticket']:
            set_text(soup, 'ticket-' + part, 'Contributor')
            set_text(soup, 'company-' + part, data['company'], size)
        elif 'Professional' in data['ticket']:
            set_text(soup, 'ticket-' + part, 'Professional')
            set_text(soup, 'company-' + part, data['company'], size)
        else:
            set_text(soup, 'ticket-' + part, data['ticket'])
            set_text(soup, 'company-' + part, '', size)

        if data['ticket'] == 'Friday Only':
            set_colour(soup, 'colour-' + part, 'a83f3f')
        elif 'Organiser' in data['ticket']:
            set_colour(soup, 'colour-' + part, '319a51')
        elif 'Volunteer' in data['ticket']:
            set_colour(soup, 'colour-' + part, '319a51')
        elif data['friday']:
            set_colour(soup, 'colour-' + part, '71319a')

        # if not data['speaker']:
        #     set_text(soup, 'speaker-' + part, '')

        icons = []
        if data['sprints']:
            icons.append(GLYPH_SPRINTS)

        # Oh, come ON! :/
        if name == 'TomEastman':
            icons.append(GLYPH_CROWN)
        elif name == 'KatieMcLaughlin':
            icons.append(GLYPH_SNOWMAN)
        elif name == 'BriannaLaugher':
            icons.append(GLYPH_STAR)

        # Really?  REALLY??!!
        elif name in ('JamesPolley', 'SachiKing'):
            icons.append(GLYPH_FLASH)

        if not data['paid']:
            icons.append('$')
        set_text(soup, 'icons-' + part, ' '.join(icons))
        set_text(soup, 'shirt-' + side, '; '.join(data['shirts']))

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
        parser.add_argument('--template', help='SVG template for creating badges',
                            default="pinaxcon/templates/badge.svg")
        parser.add_argument('--out-dir', help='Directory where SVG files will be created.',
                            default="/tmp/badges")
        parser.add_argument('usernames', nargs='*', type=str)

    def handle(self, *args, **options):

        names = list()

        orig = etree.parse(options['template'])
        tree = deepcopy(orig)
        root = tree.getroot()

        # If specific usernames were given on the command line, just use those.
        # Otherwise, use the entire list of attendees.
        if options['usernames']:
            attendee_list = AttendeeProfile.objects.filter(attendee__user__username__in=options['usernames'])
        else:
            attendee_list = AttendeeProfile.objects.all()

        print "attendees:", attendee_list

        for n, ap in enumerate(attendee_list):
            data = dict()

            at_nm = ap.name.split()
            if len(at_nm) > 0:
                data['firstname'] = at_nm[0]

                data['lastname'] = at_nm[1] if len(at_nm) > 1 else ''

            else:
                data['firstname'], data['lastname'] = ('Inego', 'Montoya')

            data['over18'] = ap.of_legal_age
            data['speaker'] = Speaker.objects.filter(user_id=ap.attendee.user.id).first() is not None

            # If the invoice is paid, fill in fields from DB.  Otherwise, we leave these
            # blank (and don't put any accesses on the badge.)
            inv = Invoice.objects.filter(user_id=ap.attendee.user.id).first()
            if inv is None or inv.is_paid == False:
                data['paid'] = data['friday'] = data['sprints'] = False
                data['shirts'] = []
                data['ticket'] = ''

            else:
                data['paid'] = inv.is_paid
                data['friday'] = inv.lineitem_set.filter(product__category__name__startswith="Specialist Day").first() is not None
                data['sprints'] = inv.lineitem_set.filter(product__category__name__startswith="Sprint Ticket").first() is not None
                try:
                    data['ticket'] = inv.lineitem_set.filter(product__category__name__startswith="Conference Ticket").first().product.name
                except:
                    data['ticket'] = '???'
                    print "ERROR:", ap.attendee.user, inv.is_paid

            try:
                data['shirts'] = [ts.product.name for ts in inv.lineitem_set.filter(product__category__name__startswith="T-Shirt")]
            except:
                data['shirts'] = list()

            data['company'] = ap.company.decode('utf8')
            data['company'] = overrides.get(data['company'], data['company'])

            generate_badge(root, data, n % 2)
            if n % 2:
                name = os.path.abspath(os.path.join(options['out_dir'], 'badge-%d.svg' % n))
                tree.write(name)
                names.append(name)
                tree = deepcopy(orig)
                root = tree.getroot()

        if not n % 2:
            name = os.path.abspath(os.path.join(options['out_dir'], 'badge-%d.svg' % n))
            tree.write(name)
            names.append(name)

        progress = progressbar.ProgressBar(widgets=[progressbar.FormatLabel(
            'Pages: %(value)s/%(max)s '
        )])
        for name in progress(names):
            subprocess.check_call(['inkscape', '-z', '-C', #'--export-text-to-path',
               '--export-pdf=%s.pdf' % name,
               '--file=' + name])

        output = os.path.join(options['out_dir'], 'all-badges.pdf')
        print 'Assembling: %s' % (output)
        files = names

        subprocess.check_call(['pdftk'] + ['%s.pdf' % n for n in names] + ['cat', 'output', output])

        return 0











