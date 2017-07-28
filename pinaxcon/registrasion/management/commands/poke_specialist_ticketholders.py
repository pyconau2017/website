
import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from registrasion.models.commerce import Invoice, LineItem
from registrasion.models.people import Attendee, AttendeeProfileBase
from django.db.models import F, Q

from registrasion.contrib.mail import send_email


class Command(BaseCommand):
    help = """Send email to ticket holders who get a free specialist day ticket but haven't yet signed up to use it."""

    def add_arguments(self, parser):
        parser.add_argument('--send-email', required=False, action="store_true", default=False,
                            help='Send email (using registration notification system) to those found.')
        parser.add_argument('--count', required=False, action='store_true', default=False,
                            help="Just say how many haven't yet signed up.")
        parser.add_argument('--kind', type=str, default="poke_unused_spec_day",
                            help="name of registrasion/emails subdir holding the templates.")

    def handle(self, *args, **options):

        # Get all of the invoices for Professional / Sponsor / Contributor
        # conference ticket holders.
        eligible = list(set([li.invoice for li in LineItem.objects.
                            filter(description__contains='Conference Ticket').
                            filter(Q(description__contains='Professional')|
                                   Q(description__contains='Contributor')|
                                   Q(description__contains='Sponsor'))]))

        # Look through these and find the ones that have no Specialist Day line item.
        pokees = dict()
        for inv in eligible:
            if not inv.lineitem_set.filter(description__contains='Specialist Day Inclusion').exists():
                ap = AttendeeProfileBase.objects.get(attendee__user_id=inv.user.id)
                pokees[inv.user.email] = ap.attendee_name()

        # Just getting a count?
        if options['count']:
            print len(pokees)
            return 0

        # Send emails?
        if options['send_email']:
            send_email([("%s <%s>" % (n,e)) for e,n in pokees.items() ], options['kind'], context={})
        else:
            # No, just print out the list in TSV form
            print "\n".join([("%s\t%s" % p) for p in pokees.items()])




