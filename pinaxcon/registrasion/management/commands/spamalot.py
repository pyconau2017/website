
'''
Spamalot - Sending Bulk Email
=============================
To send (bcc) email to conference attendees (or various,
conference-related subgroups, there is the spamalot management command:

..code-block:
 python manage.py spamalot [--count] [--send-email] [group/user name list]

Used without any options, it will print out a list of email
addresses corresponding to members of the groups (or usernames)
listed on the command line.  If no such names or groups are supplied,
this list will be empty.


To see a list of the available groups, use the --group command line switch:

..code-block:
python manage.py spamalot --group

Currently, we have:


    EVERYONE
    DJANGOGIRLS
    SPEAKERS
    VOLUNTEERS
    ATTENDEES
    FRIDAYONLY
    ORGANISERS
    NOBODY
    SPONSORS
    MAINONLY

Note: group names are case-insensitive.

To see a list of all attendees, simply put the word "attendees"
on the command line.

..code-block:
python manage.py spamalot attendees

As of this writing, you'd get a list of around 708 email addresses.

You can combine groups by just putting them on the command line:

..code-block:
python manage.py spamalot organizers volunteers

This will list email addresses for both groups.  Note that if there
are users in both groups, their email address will only appear once in this list.

If you want to add specific users or email addresses that may not be in any
of the allowed groups, just put those on the command line.  If the user
(or email address) is in the User model, the (corresponding) email address
will be added to the list.

To just get a count of the number of email addresses, add the --count switch.

Author: Nick Seidenman <nick@seidenman.net>
For PyCon AU 2017 Melbourne

'''

import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from registrasion.models.commerce import Invoice, LineItem
from registrasion.models.people import Attendee, AttendeeProfileBase
from symposion.sponsorship.models import Sponsor
from symposion.speakers.models import Speaker
from django.contrib.auth.models import User, Group

from registrasion.contrib.mail import send_email
from django.db.models import F, Q

def get_paid_up_attendees(friday=False):
    attendees = set()
    for a in Attendee.objects.distinct():
        if a.user is None:
           continue
        for inv in a.user.invoice_set.all():
            if inv.is_paid:
                if not friday or inv.lineitem_set.filter(description__contains="Specialist Day Only").exists():
                    attendees.add(a)
                    break

    return map(lambda a: a.user.email, list(attendees))

def get_DjangoGirls():
    dg_list = set()
    for u in User.objects.distinct():
        for inv in u.invoice_set.all():
            if inv.is_paid and inv.lineitem_set.filter(description__contains='DjangoGirls').exists():
                dg_list.add(u.email)
    return list(dg_list)

def get_unused_spec_day():
    '''
    This was originally in the poke_specialist_ticketholders mgt command.
    I moved it here since spamalot is a more general-purpose version
    of that anyway.
    '''
        # Get all of the invoices for Professional / Sponsor / Contributor
    # conference ticket holders.
    eligible = list(set([li.invoice for li in LineItem.objects.
                        filter(description__contains='Conference Ticket').
                        filter(Q(description__contains='Professional')|
                               Q(description__contains='Contributor')|
                               Q(description__contains='Sponsor'))]))

    # Look through these and find the ones that have no Specialist Day line item.
    attendees = set()
    for inv in eligible:
        if inv.is_paid and not inv.lineitem_set.filter(description__contains='Specialist Day Inclusion').exists():
            attendees.add(inv.user.email)

    return list(attendees)

def confirm(num):
    print """WARNING!  You are about to send email to %d users.""" % num
    return raw_input("Are you SURE you want to do this?  [N/y] -> ").upper() == 'Y'


class Command(BaseCommand):
    groups = {
        'ATTENDEES': get_paid_up_attendees,
        'SPEAKERS': lambda: [s.user.email for s in Speaker.objects.distinct() if s.user is not None],
        'SPONSORS': lambda: [s.contact_email for s in Sponsor.objects.distinct()],
        'ORGANISERS': lambda: [u.email for u in Group.objects.filter(name='Conference organisers').first().user_set.distinct()],
        'VOLUNTEERS': lambda: [u.email for u in Group.objects.filter(name='Conference volunteers').first().user_set.distinct()],
        'EVERYONE': lambda: [u.email for u in User.objects.distinct()],  # DANGER, WILL ROBINSON!!!
        'FRIDAYONLY': lambda: get_paid_up_attendees(True),
        'MAINONLY': lambda: list(set(get_paid_up_attendees(False)) - set(get_paid_up_attendees(True))),
        'DJANGOGIRLS': get_DjangoGirls,
        'UNUSEDSPECDAY': get_unused_spec_day,
        'NOBODY': lambda: list()
        }

    help = """Send (bulk) email to those (groups / individuals) listed on the command line."""

    def add_arguments(self, parser):
        parser.add_argument('--send-email', required=False, action="store_true", default=False,
                            help='Send email (using registration notification system) to those found.')
        parser.add_argument('--count', required=False, action='store_true', default=False,
                            help="Just say how many haven't yet signed up.")
        parser.add_argument('--groups', required=False, action='store_true', default=False,
                            help="List available groups.")
        parser.add_argument('--exclude', required=False, nargs='*', dest='exclusions',
                            help="Exclude this group/name/email from the resulting list.")
        parser.add_argument('--template', type=str,
                            help="name of registrasion/emails subdir holding the templates.")
        parser.add_argument('--try-bcc', type=int, required=False, default=0,
                            help="Attempt to send using bcc by chunks of specified size.  (e.g. --try-bcc=10)")
        parser.add_argument('inclusions', nargs='*', type=str)

    def build_list(self, recipients):
        '''
        Iterate through a list of groups, usernames, or email addresses.
        Include the resulting email addresses as found by group queries,
        association with usernames, or verification that the email
        address itself is associated with a valid user.
        '''
        recip_addresses = set()
        if recipients is None: return recip_addresses

        for recip in recipients:
            if recip.upper() in self.groups.keys():
                recip_addresses = recip_addresses.union(set(self.groups[recip.upper()]()))
            else:
                if '@' in recip:  # Looks like an email address ...
                    ru = User.objects.filter(email=recip).first()
                    if ru is not None:
                        recip_addresses.add(ru.email)
                else:  # Look up as if it was a username
                    ru = User.objects.filter(username=recip).first()
                    if ru is not None:
                        recip_addresses.add(ru.email)

        return recip_addresses

    def handle(self, *args, **options):

        if options['groups']:  # Just list the groups available and quit.
            print "\n".join(self.groups.keys())
            print "\nNote: group names are case-insensitive.\n"
            return 0

        # Build the list of included groups/users/emails and
        # excise any exclusions.
        inclusions = self.build_list(options['inclusions'])
        exclusions = self.build_list(options['exclusions'])

        recip_addresses = list(inclusions - exclusions)

        # Just getting a count?
        if options['count']:
            print len(recip_addresses)
            return 0

        # Send emails?
        if options['send_email']:
            if options.get('template') is None:
                print "You need to specifiy a template: --template=name-of-template"
                return 0

            if confirm(len(recip_addresses)):
                chunk = options['try_bcc']
                if chunk > 0:
                    for i in xrange(0, len(recip_addresses), chunk):
                        send_email([settings.DEFAULT_FROM_EMAIL], options['template'],
                            bcc=recip_addresses[i:i+chunk],
                            context={})
                else:
                    for recip in recip_addresses:
                        send_email([recip], options['template'], context={})
        else:
            # No, just print out the list in TSV form
            print "\n".join(recip_addresses)




