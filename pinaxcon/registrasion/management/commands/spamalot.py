
import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from registrasion.models.commerce import Invoice, LineItem
from registrasion.models.people import Attendee, AttendeeProfileBase
from symposion.sponsorship.models import Sponsor
from symposion.speakers.models import Speaker
from django.contrib.auth.models import User, Group

from registrasion.contrib.mail import send_email

def get_paid_up_attendees():
    paid_up_users = User.objects.filter(invoice__status=Invoice.STATUS_PAID)
    a_list = [a.user.email for a in Attendee.objects.distinct() \
        if a.user is not None and a.user in paid_up_users]
    return a_list

class Command(BaseCommand):
    groups = {
        'ATTENDEES': get_paid_up_attendees,
        'SPEAKERS': lambda: [s.user.email for s in Speaker.objects.distinct() if s.user is not None],
        'SPONSORS': lambda: [s.contact_email for s in Sponsor.objects.distinct()],
        'ORGANISERS': lambda: [u.email for u in Group.objects.filter(name='Conference organisers').first().user_set.distinct()],
        'VOLUNTEERS': lambda: [u.email for u in Group.objects.filter(name='Conference volunteers').first().user_set.distinct()],
        'EVERYONE': lambda: [u.email for u in User.objects.distinct()],  # DANGER, WILL ROBINSON!!!
        'NOBODY': lambda: list()
        }

    help = """Send (bulk) email to those (groups / individuals) listed on the command line."""

    def add_arguments(self, parser):
        parser.add_argument('--send-email', required=False, action="store_true", default=False,
                            help='Send email (using registration notification system) to those found.')
        parser.add_argument('--count', required=False, action='store_true', default=False,
                            help="Just say how many haven't yet signed up.")
        parser.add_argument('--template', type=str, default="spamalot_test",
                            help="name of registrasion/emails subdir holding the templates.")
        parser.add_argument('recipients', nargs='*', type=str)

    def handle(self, *args, **options):

        # Iterate through the recipients listed.   First check to see if
        # the specified recip matches one of the group names.
        # Otherwise, check usernames and email addresses.
        recip_addresses = set()
        for recip in options['recipients']:
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

        recip_addresses = list(recip_addresses)

        # Just getting a count?
        if options['count']:
            print len(recip_addresses)
            return 0

        # Send emails?
        if options['send_email']:
            send_email([settings.DEFAULT_FROM_EMAIL], options['template'], bcc=recip_addresses, context={})
        else:
            # No, just print out the list in TSV form
            print "\n".join(recip_addresses)




