import csv

import sys
import os
import csv
from lxml import etree
from copy import deepcopy
import subprocess
import progressbar

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pinaxcon.registrasion.models import AttendeeProfile
from registrasion.controllers.cart import CartController
from registrasion.controllers.invoice import InvoiceController
from registrasion.models import Voucher
from registrasion.models import Attendee
from registrasion.models import Product
from registrasion.models import Invoice

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

        if name == 'AshleyRead':
            data['ticket'] = 'Enthusiast'

        if name == 'RussellKeith-Magee' and data['dinner_tickets'] == 0:
            data['dinner_tickets'] = 1

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
        if data['dinner_tickets'] > 1:
            icons.append(GLYPH_DINNER + 'x%d' % data['dinner_tickets'])
        elif data['dinner_tickets']:
            icons.append(GLYPH_DINNER)
        if name == 'TomEastman':
            icons.append(GLYPH_CROWN)
        elif name == 'KatieMcLaughlin':
            icons.append(GLYPH_SNOWMAN)
        elif name == 'BriannaLaugher':
            icons.append(GLYPH_STAR)
        elif name in ('JamesPolley', 'SachiKing'):
            icons.append(GLYPH_FLASH)
        if not data['paid']:
            icons.append('$')
        set_text(soup, 'icons-' + part, ' '.join(icons))
        set_text(soup, 'shirt-' + side, '; '.join(data['shirts']))

class Command(BaseCommand):
    help = "Generate SVGs to print badges."

    def add_arguments(self, parser):
        parser.add_argument('--csv', help='CSV input, must include: email, name, food_needs, access_needs columns.')

    def handle(self, *args, **options):
        data = {
            'ticket': 'Organiser',
            'firstname': 'Richard Longer',
            'lastname': 'Jones',
            'company': 'Rackspace',
            'dinner_tickets': 1,
            'over18': True,
            'sprints': True,
            'speaker': True,
            'shirts': ["1 x Men's L"]
        }

        # XXX change this to reflect getting data from the DB
        #     rather than a CSV supplied via cmd line.
        with open(sys.argv[2]) as f:
            columns = f.readline().strip().split(',')
        evals = set('sprints,speaker,shirts,friday,paid,dinner_tickets,over18,printed'.split(','))

        # ``orig is the SVG template for the badge.```
        orig = etree.parse(sys.argv[1])

        names = []
        tree = deepcopy(orig)
        root = tree.getroot()

        attendees = list(csv.reader(open(sys.argv[2])))

        # firstname,lastname,company,friday,paid,shirts,ticket,sprints,dinner_tickets,over18,speaker
        # attendees.append(['Viktoriya', 'Skoryk', '', 'True', 'True', '[]', 'Guest', 'False', '1', 'True', 'False'])

        for n, badge in enumerate(attendees):
            if badge[0] == columns[0]:
                continue
            data = {k: v.replace('&#39;', "'") for k, v in zip(columns, badge)}
            try:
                for k in columns:
                    if k in evals:
                        data[k] = eval(data[k])
                    else:
                        data[k] = data[k].decode('utf8')

                data['company'] = overrides.get(data['company'], data['company'])
            except:
                print data
                raise

            generate_badge(root, data, n % 2)
            if n % 2:
                name = os.path.abspath(os.path.join(sys.argv[3], 'badge-%d.svg' % n))
                tree.write(name)
                names.append(name)
                tree = deepcopy(orig)
                root = tree.getroot()

        if not n % 2:
            name = os.path.abspath(os.path.join(sys.argv[3], 'badge-%d.svg' % n))
            tree.write(name)
            names.append(name)

        progress = progressbar.ProgressBar(widgets=[progressbar.FormatLabel(
            'Pages: %(value)s/%(max)s '
        )])
        for name in progress(names):
            subprocess.check_call(['inkscape', '-z', '-C', #'--export-text-to-path',
               '--export-pdf=%s.pdf' % name,
               '--file=' + name])

        output = 'badges.pdf'
        print 'Assembling: %s' % (output)
        files = names
        # files = [
        #     'badge-back.pdf' if i % 2 else '%s.pdf' % names[i // 2]
        #     for i in range(len(names) * 2)
        # ]

        subprocess.check_call(['pdftk'] + ['%s.pdf' % n for n in names] + ['cat', 'output', output])

        def created_or_found(created):
            return "created" if created else "found"












