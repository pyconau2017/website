import csv

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Registers a list of people with a django girls ticket. If someone already has a ticket, won't change that."

    def add_arguments(self, parser):
        parser.add_argument('--csv', help='CSV input, must include: email, name, food_needs, access_needs columns.')

    def handle(self, *args, **options):

        details = {}
        with open(options['csv'], 'r') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=None)
            for row in reader:
                details[row['email']] = row

        for email in details.keys():
            user, created = User.objects.get_or_create(username=email, email=email)

            print("%s user %s" % (email, "created" if created else "found"))

            # Lookup...paid carts?
