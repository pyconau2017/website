import csv
import datetime

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pinaxcon.registrasion.models import AttendeeProfile
from registrasion.controllers.invoice import InvoiceController
from registrasion.models import Attendee
from registrasion.models import Product
from registrasion.models import Invoice

class Command(BaseCommand):
    help = "Registers a list of people with a django girls ticket. If someone already has a ticket, won't change that."

    def add_arguments(self, parser):
        parser.add_argument('--csv', help='CSV input, must include: email, name, food_needs, access_needs columns.')

    def handle(self, *args, **options):

        djangoticket = Product.objects.filter(name="DjangoGirls")[0]

        details = []
        with open(options['csv'], 'r') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=None)
            for row in reader:
                details.append(row)

        for detail in details:
            email = detail['email']

            user, created = User.objects.get_or_create(username=email, email=email)

            print("%s user %s" % (email, created_or_found(created)))

            attendee, created = Attendee.objects.get_or_create(user=user)

            print("%s attendee %s" % (email, created_or_found(created)))

            profile, created = AttendeeProfile.objects.get_or_create(
                attendee=attendee,
                name=detail['name'],
                accessibility_requirements=detail['access_needs'],
                dietary_restrictions=detail['food_needs'],
                lca_announce=False,
                linux_australia=False,
            )

            print("%s profile %s" % (email, created_or_found(created)))

            ticket_purchased = False
            for invoice in Invoice.objects.filter(user=user, status=Invoice.STATUS_PAID):
                for lineitem in invoice.lineitem_set.filter(product=djangoticket):
                    ticket_purchased = True

            if ticket_purchased:
                print("%s django ticket already purchased" % (email))

            else:
                due = datetime.timedelta(days=1)

                invoice = InvoiceController.manual_invoice(user, due, [(djangoticket, 1)])
                InvoiceController(invoice)._mark_paid()

                print("%s django ticket purchased" % email)

            print("\n")


def created_or_found(created):
    return "created" if created else "found"
